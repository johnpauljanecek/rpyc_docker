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
        self._browser = self.conn.modules["rpyc_docker.browser"].Browser()
        self._browser.setup(driver = driver,
                           visible = visible,
                           backend = backend,
                           displayArgs = displayArgs)
        self._driver = self.browser.driver
        return True

    def start_openbox(self,password = "secret",size = (1024,600),color_depth = 24):
        self.create_vnc_passwd(password)
        xstartupLines = ['#!/bin/sh',
                 '',
                 '# Uncomment the following two lines for normal desktop:',
                 '# unset SESSION_MANAGER',
                 '# exec /etc/X11/xinit/xinitrc',
                 '',
                 '[ -x /etc/vnc/xstartup ] && exec /etc/vnc/xstartup',
                 '[ -r $HOME/.Xresources ] && xrdb $HOME/.Xresources',
                 'xsetroot -solid grey',
                 'vncconfig -iconic &',
                 #'x-terminal-emulator -geometry 80x24+10+10 -ls -title "$VNCDESKTOP Desktop" &',
                 'openbox-session &']
        
        #self.write_file("/root/.vnc/xstartup","\n".join(xstartupLines))
        
        self.vncserver_exec_id = self.docker.exec_create(
                self.container,
                "vncserver -geometry %dx%d -depth %d :0" % (size[0],size[1],color_depth), 
                stdout=False, 
                stderr=False,
                tty=False,
            )

        self.docker.exec_start(self.vncserver_exec_id,
                                   detach=True,
                                   stream=False)
    
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

