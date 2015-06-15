from selenium import webdriver
from rpyc_docker.drivers import WebDriver
import shutil,random,string

class TamperMonkey(WebDriver):
    def __init__(self,chromeDriverPath = None,profileDir = None,**kwargs):
        """
        chromeDriverPath is path to Chrome Driver
        """
        WebDriver.__init__(self,**kwargs)
        self.chromeDriverPath = chromeDriverPath
        self.profileDir = profileDir
        if not profileDir :
            self.profileDir = "/Development/chrome_profiles/tampermonkey"
        
    def setup(self):
        self.tmpProfileDir = "/tmp/%s" % ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        shutil.copytree(self.profileDir,self.tmpProfileDir)

        self.chromeOptions = webdriver.ChromeOptions()
        self.chromeOptions.add_argument("user-data-dir=%s" % self.tmpProfileDir)
        if self.browserBinary:
            self.chromeOptions.binary_location = self.browserBinary

        if self.browserBinary:
            self.chromeOptions.binary_location = self.browserBinary
        
        if self.chromeDriverPath :
            self.driver = webdriver.Chrome(
                executable_path = self.chromeDriverPath,
                chrome_options = self.chromeOptions,
            )
        else :
            self.driver = webdriver.Chrome(chrome_options = self.chromeOptions)
        return True

