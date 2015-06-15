from rpyc_docker.rpyc_worker import RpycWorker
from rpyc_docker.worker import decorator_reset_uptime
import rpyc_docker.browser,os.path
import logging,rpyc,rpyc.utils.classic

class BrowserRpycWorker(RpycWorker):
    def __init__(self,docker,mount = None):
        RpycWorker.__init__(self,docker,mount)
        self._browser = None
        self._driver = None

    @property
    @decorator_reset_uptime
    def driver(self):
        return self._driver

    @property
    @decorator_reset_uptime
    def browser(self):
        return self._browser
        
    @decorator_reset_uptime
    def setup_browser(self,driver,visible = False,backend = 'xvfb',displayArgs={}):
        
        # rpyc.utils.classic.upload_file(self.conn,os.path.abspath(rpyc_docker.browser.__file__),"/root/browser.pyc")
        # self._browser = self.conn.modules["browser"].Browser()
        self.browser.setup(driver = driver,
                           visible = visible,
                           backend = backend,
                           displayArgs = displayArgs)
        self._driver = self.browser.driver
        return True

    def dump_page(self,destDir):        
        import os.path
        import datetime
        dt = datetime.datetime.now().isoformat()
        fName = "%s-%s.html" % (dt,driver.title)
        fName = os.path.join(destDir,fName)
        with open(f_name,'w') as file_:
            file_.write(driver.page_source)
        self.driver.get_screenshot_as_file("%s-%s.png" % (dt,driver.title))
        return True

