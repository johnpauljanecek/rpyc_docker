import threading,time,os,traceback,logging
from subprocess import check_output,CalledProcessError
logger = logging.getLogger("rpyc_docker")
logger.setLevel(logging.INFO)

class Worker(threading.Thread):
    _numWorkers = 0
    _numWorkersLock = threading.Lock()

    def __init__(self):
        threading.Thread.__init__(self)
        self.status = "init"
        self.result = None
        self.traceback = None
        self.workerNum = self.inc_workers()
        self._startTime = time.time()

    def cmd(self,cmd):
        try:
            output = check_output(cmd,shell = True)
            return (0,cmd,output)
        except CalledProcessError as e:
            return (e.returncode,e.cmd,e.output)

    @property
    def upTime(self):
        return time.time() - self._startTime

    def setup(self):
        pass

    def teardown(self):
        pass

    def run(self):
        try:
            self.status = "running"
            self.result = self.work()
            self.status = "done"
        except Exception as e:
            self.traceback = traceback.format_exc()
            self.status = "error"

    def work(self):
        pass
    
    @classmethod
    def inc_workers(cls):
        Worker._numWorkersLock.acquire()
        Worker._numWorkers += 1
        Worker._numWorkersLock.release()
        return Worker._numWorkers
