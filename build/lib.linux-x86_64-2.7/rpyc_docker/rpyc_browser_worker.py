from rpyc_docker.rpyc_worker import RpycWorker
import rpyc_docker.browser,os.path

import logging,rpyc,rpyc.utils.classic
logger = logging.getLogger("rpyc_docker")
logger.setLevel(logging.INFO)

class BrowserRpycWorker(RpycWorker):
    def __init__(self,docker,mount = None):
        RpycWorker.__init__(self,docker,mount)

    def setup_browser(self,driver,visible = False,backend = 'xvfb'):
        
        rpyc.utils.classic.upload_file(self.conn,os.path.abspath(rpyc_docker.browser.__file__),"/root/browser.pyc")
        self.browser = self.conn.modules["browser"].Browser()
        self.browser.setup(driver = driver,
                           visible = visible,
                           backend = backend)
        self.driver = self.browser.driver
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

