import seleniumrequests,os
from rpyc_docker.drivers import WebDriver
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

class Chrome(WebDriver):
    def __init__(self):
        WebDriver.__init__(self,**kwargs)

    def setup(self):
        self.driver = seleniumrequests.Firefox()
        return self.driver
    
class FireFox(WebDriver):
    def __init__(self):
        WebDriver.__init__(self,**kwargs)

    def setup(self):
        self.driver = seleniumrequests.Firefox()
        return self.driver

class FireFoxRequests(WebDriver):
    fireFoxPath = "/home/john/Development/firefox_exe/firefox_35.0/firefox-bin"
    extensionDir = "/home/john/Development/amazon/firefox_extensions"
    extensions = [("firebug","firebug@software.joehewitt.com.xpi"),]
    def __init__(self):
        WebDriver.__init__(self,browserBinary = self.fireFoxPath)
        
    def load_extensions(self):
        for name,ext_path in self.extensions:
            self.firefoxProfile.add_extension(os.path.join(self.extensionDir,ext_path))
        
    def setup_profile(self):
        if self.browserBinary :
            self.firefoxBinary = FirefoxBinary(self.browserBinary)
            
        self.firefoxProfile = webdriver.FirefoxProfile(self.profileDir)
        self.load_extensions()
        
        if self.userAgent :
            self.firefoxProfile.set_preference("general.useragent.override",self.userAgent);
    
    def setup(self):
        self.setup_profile()
        if self.browserBinary :
            self.driver = seleniumrequests.Firefox(firefox_binary = self.firefoxBinary,firefox_profile = self.firefoxProfile)
        else :
            self.driver = seleniumrequests.Firefox(firefox_binary = self.firefoxBinary,firefox_profile = self.firefoxProfile)
        return self.driver
