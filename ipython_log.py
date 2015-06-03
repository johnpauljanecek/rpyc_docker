# IPython log file

get_ipython().magic(u'pwd ')
get_ipython().magic(u'cd ..')
import worker
import rpyc_docker.worker
import rpyc_docker.worker
reload(rpyc_docker.worker)
import rpyc_docker.worker
reload(rpyc_docker.worker)
from rpyc_docker import Worker
import rpyc_docker.worker
reload(rpyc_docker.worker)
import rpyc_docker.rpyc_browser_worker
from rpyc_docker import BrowserRpycWorker
import time
from reddit_page import RedditPage

class RedditWorker(BrowserRpycWorker):
    def __init__(self,docker,subReddit,redditResultQueue):
        BrowserRpycWorker.__init__(self,docker)
        self.subReddit = subReddit
        self.redditResultQueue = redditResultQueue
        
    def work(self):
        self.create_container()
        time.sleep(2)
        self.setup_browser("firefox")
        redditPage = RedditPage(self.browser)
        redditPage.goto_subreddit(self.subReddit)
        results = redditPage.get_reddit_titles()
        self.redditResultQueue.put([self.subReddit,results])
        return True
get_ipython().magic(u'cd examples/')
import time
from reddit_page import RedditPage

class RedditWorker(BrowserRpycWorker):
    def __init__(self,docker,subReddit,redditResultQueue):
        BrowserRpycWorker.__init__(self,docker)
        self.subReddit = subReddit
        self.redditResultQueue = redditResultQueue
        
    def work(self):
        self.create_container()
        time.sleep(2)
        self.setup_browser("firefox")
        redditPage = RedditPage(self.browser)
        redditPage.goto_subreddit(self.subReddit)
        results = redditPage.get_reddit_titles()
        self.redditResultQueue.put([self.subReddit,results])
        return True
import rpyc_docker.worker
reload(rpyc_docker.worker)
import rpyc_docker.rpyc_browser_worker
from rpyc_docker import BrowserRpycWorker
get_ipython().magic(u'cd ..')
import rpyc_docker.worker
reload(rpyc_docker.worker)
import rpyc_docker.rpyc_browser_worker
from rpyc_docker import BrowserRpycWorker
import time
from reddit_page import RedditPage

class RedditWorker(BrowserRpycWorker):
    def __init__(self,docker,subReddit,redditResultQueue):
        BrowserRpycWorker.__init__(self,docker)
        self.subReddit = subReddit
        self.redditResultQueue = redditResultQueue
        
    def work(self):
        self.create_container()
        time.sleep(2)
        self.setup_browser("firefox")
        redditPage = RedditPage(self.browser)
        redditPage.goto_subreddit(self.subReddit)
        results = redditPage.get_reddit_titles()
        self.redditResultQueue.put([self.subReddit,results])
        return True
get_ipython().magic(u'cd ..')
import rpyc_docker.worker
reload(rpyc_docker.worker)
import rpyc_docker.rpyc_browser_worker
reload(rpyc_docker.rpyc_browser_worker)
from rpyc_docker import BrowserRpycWorker
get_ipython().magic(u'pwd ')
get_ipython().magic(u'cd rpyc_docker/')
get_ipython().magic(u'cd ..')
import rpyc_docker.worker
reload(rpyc_docker.worker)
import rpyc_docker.rpyc_browser_worker
reload(rpyc_docker.rpyc_browser_worker)
from rpyc_docker import BrowserRpycWorker
import rpyc_docker.worker
reload(rpyc_docker.worker)
import rpyc_docker.rpyc_browser_worker
reload(rpyc_docker.rpyc_browser_worker)
from rpyc_docker import BrowserRpycWorker
get_ipython().magic(u'cd rpyc_docker/')
import rpyc_docker.worker
reload(rpyc_docker.worker)
import rpyc_docker.rpyc_browser_worker
reload(rpyc_docker.rpyc_browser_worker)
from rpyc_docker import BrowserRpycWorker
import time
from reddit_page import RedditPage

class RedditWorker(BrowserRpycWorker):
    def __init__(self,docker,subReddit,redditResultQueue):
        BrowserRpycWorker.__init__(self,docker)
        self.subReddit = subReddit
        self.redditResultQueue = redditResultQueue
        
    def work(self):
        self.create_container()
        time.sleep(2)
        self.setup_browser("firefox")
        redditPage = RedditPage(self.browser)
        redditPage.goto_subreddit(self.subReddit)
        results = redditPage.get_reddit_titles()
        self.redditResultQueue.put([self.subReddit,results])
        return True
import rpyc_docker.worker
reload(rpyc_docker.worker)
import rpyc_docker.rpyc_browser_worker
reload(rpyc_docker.rpyc_browser_worker)
import rpyc_docker.manager
from rpyc_docker import BrowserRpycWorker
from rpyc_docker import Manager
import time
from reddit_page import RedditPage

class RedditWorker(BrowserRpycWorker):
    def __init__(self,docker,subReddit,redditResultQueue):
        BrowserRpycWorker.__init__(self,docker)
        self.subReddit = subReddit
        self.redditResultQueue = redditResultQueue
        
    def work(self):
        self.create_container()
        time.sleep(2)
        self.setup_browser("firefox")
        redditPage = RedditPage(self.browser)
        redditPage.goto_subreddit(self.subReddit)
        results = redditPage.get_reddit_titles()
        self.redditResultQueue.put([self.subReddit,results])
        return True
import queue
import Queue
redditResultQueue = Queue.Queue()
workQueue = Queue.Queue()
from docker import Client
docker = Client(base_url='unix://var/run/docker.sock')
redditQueries = ["/r/python","/r/clojure","r/programming","r/javascript"]
for redditQuery in redditQueries :
    workQueue.put([docker,RedditWorker,redditResultQueue],{})
manager = Manager(workQueue,1)
manager.start()
manager.report()
import rpyc_docker.worker
reload(rpyc_docker.worker)
import rpyc_docker.rpyc_browser_worker
reload(rpyc_docker.rpyc_browser_worker)
import rpyc_docker.manager
from rpyc_docker import BrowserRpycWorker
from rpyc_docker import Manager
import rpyc_docker.worker
reload(rpyc_docker.worker)
import rpyc_docker.rpyc_browser_worker
reload(rpyc_docker.rpyc_browser_worker)
import rpyc_docker.manager
reload(rpyc_docker.manager)
from rpyc_docker import BrowserRpycWorker
from rpyc_docker import Manager
workQueue = Queue.Queue()
redditQueries = ["/r/python","/r/clojure","r/programming","r/javascript"]
for redditQuery in redditQueries :
    workQueue.put([docker,RedditWorker,redditResultQueue],{})
redditQueries = ["/r/python","/r/clojure","r/programming","r/javascript"]
for redditQuery in redditQueries :
    workQueue.put([docker,RedditWorker,redditResultQueue],{})
workQueue = Queue.Queue()
redditQueries = ["/r/python","/r/clojure","r/programming","r/javascript"]
for redditQuery in redditQueries :
    workQueue.put([docker,RedditWorker,redditResultQueue],{})
manager = Manager(workQueue,1)
manager.start()
manager.report()
manager.traceback
manager.traceback.splitlines()
import rpyc_docker.worker
reload(rpyc_docker.worker)
import rpyc_docker.rpyc_browser_worker
reload(rpyc_docker.rpyc_browser_worker)
import rpyc_docker.manager
reload(rpyc_docker.manager)
from rpyc_docker import BrowserRpycWorker
from rpyc_docker import Manager
manager = Manager(workQueue,1)
manager.start()
manager.report()
get_ipython().magic(u'logon')
get_ipython().magic(u'logon')
get_ipython().magic(u'logstart')
manager = Manager(workQueue,1)
manager.start()
manager.report()
import logging
logger = logging.getLogger("rpyc_docker")
logger.setLevel(logging.INFO)
logger.info("AAAAAAAAAAA")
redditQueries = ["/r/python","/r/clojure","r/programming","r/javascript"]
for redditQuery in redditQueries :
    workQueue.put([docker,RedditWorker,redditResultQueue],{})
workQueue = Queue.Queue()
redditQueries = ["/r/python","/r/clojure","r/programming","r/javascript"]
for redditQuery in redditQueries :
    workQueue.put([docker,RedditWorker,redditResultQueue],{})
manager = Manager(workQueue,1)
manager.start()
manager.report()
workQueue = Queue.Queue()
redditQueries = ["/r/python","/r/clojure","r/programming","r/javascript"]
for redditQuery in redditQueries :
    workQueue.put([RedditWorker,[docker,redditResultQueue],{}])
manager = Manager(workQueue,1)
manager.start()
manager.report()
manager.traceback.splitlines()
redditResultQueue = Queue.Queue()
workQueue = Queue.Queue()
redditQueries = ["/r/python","/r/clojure","r/programming","r/javascript"]
for redditQuery in redditQueries :
    workQueue.put([RedditWorker,[docker,redditQuery,redditResultQueue],{}])
manager = Manager(workQueue,1)
manager.start()
manager.report()
manager.errors[0]
manager.errors[0].spitlines()
manager.errors[0].splitlines()
manager.errors[0]
manager.errors[0][0].splitlines()
manager.report()
