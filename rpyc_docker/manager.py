import Queue,threading,time,os,traceback,subprocess,rpyc,logging
from docker.utils import create_host_config
from subprocess import check_output,CalledProcessError

logger = logging.getLogger("rpyc_docker")
logger.setLevel(logging.INFO)

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

        self.workers = []
        self._results = []
        self._errors = []

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
    
    def __run(self):
        while self.running:
            runningWorkers = []
            doneWorkers = []
            for worker,workerCls,args,kwArgs in self.workers :
                if worker.upTime > self.maxTime :
                    self._errors.append(["timeout",workerCls,args,kwArgs])
                    doneWorkers.append(worker)
                elif worker.status == "running" :
                    runningWorkers.append([worker,workerCls,args,kwArgs])
                elif worker.status == "done" :
                    self._results.append([worker.result,workerCls,args,kwArgs])
                    doneWorkers.append(worker)
                elif worker.status == "error" :
                    self._errors.append([worker.traceback,workerCls,args,kwArgs])
                    doneWorkers.append(worker)
                else :
                    pass
            
            for worker in doneWorkers :
                worker.teardown()
            self.workers = runningWorkers
            
            for n in range(self.numWorkers - len(self.workers)) :
                try:
                    workerCls,args,kwArgs = self.argQueue.get_nowait()
                    logger.info("%s,%s,%s" % (workerCls,args,kwArgs))
                    worker = workerCls(*args,**kwArgs)
                    self.workers.append([worker,workerCls,args,kwArgs])
                    worker.start()
                except Queue.Empty:
                    break
            
            if len(self.workers) == 0 :
                self.running = False
            
            time.sleep(1)
                
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
        return self._errors[n][0]

    def get_result(self,n):
        """
        returns the result of a worker if it has finished

        :param n: worker number
        :type n: int
        :return: result
        :rtype: object:
        """
        return self._results[n][0]
    
        


