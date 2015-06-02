#browser.py
#part of docker_rpyc
from selenium import webdriver
from pyvirtualdisplay import Display
import os.path,os,datetime,logging

logger = logging.getLogger("rpyc_docker")
logger.setLevel(logging.INFO)

class Browser(object):
    def __init__(self):
        self.display = None
        self.driver = None
        self.start = datetime.datetime.now().strftime("%b-%d-%Y-%H:%M:%S")

    def driver_chrome(self):
        self.driver = webdriver.Chrome(executable_path='/usr/lib/chromium-browser/chromedriver')
        return "chrome"

    def driver_firefox(self):
        self.driver = webdriver.Firefox()
        return "firefox"

    def patch_pydisplay(self):
        """patch xvnc to use password file"""
        from pyvirtualdisplay.xvnc import XvncDisplay
        import pexpect

        child = pexpect.spawn('vncpasswd')
        child.expect('Password:')
        child.sendline('secret')
        child.expect('Verify:')
        child.sendline('secret')

        @property
        def _cmd(self):
            cmd = ['Xvnc',
                   '-depth', str(self.color_depth),
                   '-geometry', '%dx%d' % (self.size[0], self.size[1]),
                   '-rfbport', str(self.rfbport),
                   '-rfbauth', '/root/.vnc/passwd',
                   self.new_display_var,
               ]
            return cmd
        XvncDisplay._cmd = _cmd

    def setup(self,visible = False,
              driver = "firefox",
              backend = 'xvfb',
              opt = None):
        """
        driver is either a function which creates a webdriver
        or an attribute string
        visible is either True or False, if False it uses pydisplay
        backend only is used if visible is False, can be either 'xvfb' or 'xvnc'
        """
        if backend == "xvnc" :
            self.patch_pydisplay()

        if not visible :
            if backend == 'xvfb':
                self.display = Display(backend=backend)
            else :
                self.display = Display(backend=backend,rfbport = 5900)
            self.display.start()
        try:
            self.driver = driver()
        except TypeError:
            try:
                return getattr(self,"driver_%s" % (driver,))()
            except AttributeError:
                self.teardown()
                return False

    def teardown(self):
        if self.driver :
            self.driver.quit()
            self.driver = None

        if self.display :
            self.display.stop()
            self.display = None
        return True

    def js_ex(self,script,*args):
        return self.driver.execute_script(script,*args)

    def js_ex_file(self,fileName):
        with file(fileName,"r") as f :
            script = f.read()
            return self.driver.execute_script(script)

    def get_attributes(self,element):
        """gets all of the attributes of a selenium web element"""
        return self.driver.execute_script("""
        var items = {}; 
        for (index = 0; index < arguments[0].attributes.length; ++index) 
        { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;""",
                                          element)

    def get_element_image(self,element):
        """takes screenshot of an element returns it as a PIL image
        on IPython notebook the PIL image will be automatically 
        displayed. Requires that PIL or Pillows is installed
        """
        from PIL import Image
        from StringIO import StringIO
        location = element.location
        size = element.size
        img = Image.open(StringIO(self.driver.get_screenshot_as_png()))
        left = int(location['x'])
        top = int(location['y'])
        right = int(location['x'] + size['width'])
        bottom = int(location['y'] + size['height'])
        img = img.crop((left, top, right, bottom))
        return img
