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
        self.traceback = None
        
        self.argQueue = argQueue
        self.numWorkers = numWorkers
        self.maxTime = maxTime

        self.workers = []
        self.results = []
        self.errors = []

    def run(self):
        try:
            self.__run()
        except Exception:
            self.traceback = traceback.format_exc()
            self.running = False
            
    def stop(self):
        self.running = False
    
    def __run(self):
        while self.running:
            runningWorkers = []
            doneWorkers = []
            for worker,workerCls,args,kwArgs in self.workers :
                if worker.upTime > self.maxTime :
                    self.errors.append(["timeout",workerCls,args,kwArgs])
                    doneWorkers.append(worker)
                elif worker.status == "running" :
                    runningWorkers.append([worker,workerCls,args,kwArgs])
                elif worker.status == "done" :
                    self.results.append([worker.result,workerCls,args,kwArgs])
                    doneWorkers.append(worker)
                elif worker.status == "error" :
                    self.errors.append([worker.traceback,workerCls,args,kwArgs])
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
        result = [
            "WorkerManager Report",
            "Running workers %d " % len(self.workers),
            "Results %d " % len(self.results),
            "Errors %d " % len(self.errors),
            "Queue Size %d" % self.argQueue.qsize()
        ]        

        if self.traceback:
            result.append("TRACEBACK ERROR")
            result.append(self.traceback)
        
        return "\n".join(result)


