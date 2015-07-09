import Queue,threading,time,os,traceback,subprocess,rpyc,logging
try:
    from docker.utils import create_host_config
except ImportError:
    pass
from subprocess import check_output,CalledProcessError

logger = logging.getLogger("rpyc_docker")
logger.setLevel(logging.INFO)

class WorkerResult(object):
    def __init__(self):
        self._cls = None
        self._args = None
        self._kwargs = None
        self._traceback = None
        self._logfile = None
        self._status = None
        self._result = None

    @property
    def cls(self):
        return self._cls

    @cls.setter
    def cls(self, value):
        self._cls = value

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, value):
        self._args = value

    @property
    def kwargs(self):
        return self._kwargs

    @kwargs.setter
    def kwargs(self, value):
        self._kwargs = value

    @property
    def traceback(self):
        return self._traceback

    @traceback.setter
    def traceback(self,value):
        self._traceback = value

    @property
    def logfile(self):    
        return self._logfile

    @logfile.setter
    def logfile(self,value):    
        self._logfile = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self,value):
        self._status = value

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self,value):
        self._result = value


class WorkQueue(Queue.Queue):
    def __init__(self):
        Queue.Queue.__init__(self)
    
    def put_work(self,cls,args,kwArgs):
        self.put([cls,args,kwArgs])

class DeadWorkerThread(threading.Thread):
    def __init__(self,deadWorkersQueue):
        threading.Thread.__init__(self)
        self.deadWorkersQueue = deadWorkersQueue
        self.running = True

    def run(self):
        while self.running :
            try:
                worker = self.deadWorkersQueue.get(True,timeout = 1.0)
                worker.teardown()
            except Queue.Empty:
                pass

class Manager(threading.Thread):
    def __init__(self,argQueue,numWorkers,maxTime = 300):
        """
        argQueue cls [args] {kwArgs}
        """
        threading.Thread.__init__(self)
        self.running = True
        self._traceback = None
        
        self.argQueue = argQueue
        self.numWorkers = numWorkers
        self.maxTime = maxTime
        self._loopDelay = 0.5 #how often to poll the loop
    
        self.workers = []
        self._results = []
        self._errors = []
        # self.deadWorkersQueue = Queue.Queue()
        # self._deadWorkerThread = DeadWorkerThread(self.deadWorkersQueue)
        # self._deadWorkerThread.start()

    
    def run(self):
        try:
            self.__run()
        except Exception:
            self._traceback = traceback.format_exc()
            self.running = False
            
    def stop(self):
        """
        stops the manager, there might be a delay before it loops throught the workers
        """
        self.running = False
        #self._deadWorkerThread.running = False
    
    def __run(self):
        while self.running:
            runningWorkers = []
            doneWorkers = []
            for worker,workerCls,args,kwArgs in self.workers :
                if worker.upTime > self.maxTime :
                    self._errors.append([worker,workerCls,args,kwArgs])
                    worker.traceback = "timeout"
                    doneWorkers.append(worker)
                elif worker.status == "running" :
                    runningWorkers.append([worker,workerCls,args,kwArgs])
                elif worker.status == "done" :
                    self._results.append([worker,workerCls,args,kwArgs])
                    #self._results.append([worker.result,workerCls,args,kwArgs])
                    doneWorkers.append(worker)
                elif worker.status == "error" :
                    self._errors.append([worker,workerCls,args,kwArgs])
                    #self._errors.append([worker.traceback,workerCls,args,kwArgs])
                    doneWorkers.append(worker)
                else :
                    pass
            
            self.workers = runningWorkers
            
            for i in range(self.numWorkers - len(self.workers)):
                try:
                    workerCls,args,kwArgs = self.argQueue.get_nowait()
                    logger.info("%s,%s,%s" % (workerCls,args,kwArgs))
                    worker = workerCls(*args,**kwArgs)
                    self.workers.append([worker,workerCls,args,kwArgs])
                    worker.start()
                except Queue.Empty:
                    break
            
            #start new workers before we destroy old ones
            for worker in doneWorkers :
                #self.deadWorkersQueue.put(worker)
                worker.teardown()
                    
            if len(self.workers) == 0 :
                self.running = False
            
            #put in to slow down the creation of workers
            # try:
            #     deadWorker = self.deadWorkersQueue.get_nowait()
            #     deadWorker.teardown()
            # except Queue.Empty:
            #     pass
            self.main_thread_callback()
            time.sleep(self._loopDelay)

    def main_thread_callback(self):
        """
        This is called every time the check thread does a loop
        """
        pass
                
    def report(self):
        """
        generates report of the status of the manager
        
        :return: report
        :rtype: string
        """
        result = [
            "WorkerManager Report",
            "Running workers %d " % len(self.workers),
            "Results %d " % len(self._results),
            "Errors %d " % len(self._errors),
            "Queue Size %d" % self.argQueue.qsize()
        ]        

        if self._traceback:
            result.append("TRACEBACK ERROR")
            result.append(self._traceback)
        
        return "\n".join(result)

    @property
    def managerTraceback(self):
        """
        shows traceback of manager if it has crashed
        
        :return: traceback of manager
        :rtype: string
        """
        return self._traceback

    def get_error(self,n):
        """
        returns the traceback of a worker if it has crashed

        :param n: worker number
        :type n: int
        :return: traceback
        :rtype: str:
        """
        worker = self._errors[n][0]
        return worker.traceback

    def get_result(self,n):
        """
        returns the result of a worker if it has finished

        :param n: worker number
        :type n: int
        :return: result
        :rtype: object:
        """
        worker = self._results[n][0]
        return worker.result

    def get_worker_result(self,n):
        return self._results[n][0]

    def get_worker_error(self,n):
        return self._errors[n][0]
