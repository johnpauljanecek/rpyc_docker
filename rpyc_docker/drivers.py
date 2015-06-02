#drivers.py
#part of docker_rpyc
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

class WebDriver(object):
    def __init__(self,browserBinary = None,profileDir = None,userAgent = None):
        self.userAgent = userAgent
        self.profileDir = profileDir
        self.browserBinary = browserBinary
        self.driver =  None
                
    def get_userAgent(self):
        return self.driver.execute_script("return navigator.userAgent;")
    
    def setup(self):
        pass
    
    def __call__(self):
        self.setup()
        return self.driver

class ChromeDriver(WebDriver):
    def __init__(self,chromeDriverPath = None,**kwargs):
        """
        chromeDriverPath is path to Chrome Driver
        """
        WebDriver.__init__(self,**kwargs)
        self.chromeDriverPath = chromeDriverPath
    
    """
    http://simply-tutorial.com/blog/2014/07/10/selenium-webdriver-set-browsers-user-agent-and-proxy/
    chrome://about/ #lists chrome urls
    """
    
    def get_plugins(self):
        #driver.get("chrome://plugins/")
        pass
        
    def setup(self):
        self.chromeOptions = webdriver.ChromeOptions()
        
        if self.userAgent :
            self.chromeOptions.add_argument("user-agent=%s" % self.userAgent)

        
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

class FirefoxDriver(WebDriver):
    def __init__(self,**kwargs):
        WebDriver.__init__(self,**kwargs)
        
    def setup_profile(self):
        if self.browserBinary :
            self.firefoxBinary = FirefoxBinary(self.browserBinary)
            
        self.firefoxProfile = webdriver.FirefoxProfile(self.profileDir)
        
        if self.userAgent :
            self.firefoxProfile.set_preference("general.useragent.override",self.userAgent);
    
    def setup(self):
        self.setup_profile()

        if self.browserBinary :
            self.driver = webdriver.Firefox(firefox_binary = self.firefoxBinary,firefox_profile = self.firefoxProfile)
        else :
            self.driver = webdriver.Firefox(firefox_profile = self.firefoxProfile)
        
        return self.driver
