import threading,time,os,traceback,logging
from subprocess import check_output,CalledProcessError
from functools import wraps
#logger = logging.getLogger("rpyc_docker")
#logger.setLevel(logging.INFO)

def decorator_reset_uptime(f):
    @wraps(f)
    def wrapper(*args,**kwargs):
        self = args[0]
        self.reset_uptime()
        return f(*args,**kwargs)
    return wrapper

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

    def reset_uptime(self):
        self._startTime = time.time()

    @property
    def upTime(self):
        """
        used by manager to see if the worker has timed out
        """
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
