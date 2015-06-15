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
        logger.info("def driver_firefox(self):")
        self.driver = webdriver.Firefox()
        return "firefox"

    def patch_pydisplay(self):
        """
        monkey patch xvnc to use password file
        if using xvnc backend call this function before calling setup
        """
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
              opt = None,displayArgs={}):
        """
        Sets up the webbrowser

        :param visible: if True, visible if False runs as headless
        :param driver: either "firefox" or "chrome" or a an instance of rpyc_docker.drivers.WebDriver
        :param backend: either "xvfb" or xvnc" if xvnc then it will start and xvnc server which can be connected to. Default password is secret.
        :param opt: not used
        :param displayArgs: extra configurations passed to from pyvirtualdisplay import Display 
        :type visible: bool
        :type driver: str or rpyc_docker.drivers.WebDriver
        :type backend: str
        :type opt: None
        :type displayArgs: {}
        :return: True if successful
        :rtype: bool
        """
        if backend == "xvnc" :
            self.patch_pydisplay()

        if not visible :
            if backend == 'xvfb':
                self.display = Display(backend=backend,**displayArgs)
            else :
                self.display = Display(backend=backend,rfbport = 5900,**displayArgs)
            self.display.start()
        try:
            self.driver = driver()
            return True
        except TypeError:
            try:
                getattr(self,"driver_%s" % (driver,))()
                return True
            except AttributeError:
                self.teardown()
                return False

    def teardown(self):
        """
        tears down the webbrowser
        """
        if self.driver :
            self.driver.quit()
            self.driver = None

        if self.display :
            self.display.stop()
            self.display = None
        return True

    def js_ex(self,script,*args):
        """
        convenience function to execute javascript.

        :param script: The JavaScript to execute.
        :param *args: Any applicable arguments for your JavaScript.
        """
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
