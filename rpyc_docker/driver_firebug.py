from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from rpyc_docker.drivers import WebDriver
import os.path

class FirefoxGreaseMonkey(WebDriver):
    fireFoxPath = "/Development/firefox_exe/firefox_36.0/firefox-bin"
    greaseMonkeyProfile = "/Development/tmp/greasemonkey_36"
    #greaseMonkeyProfile = "/Development/tmp/greasemonkey"
    def __init__(self):
        WebDriver.__init__(self,browserBinary = self.fireFoxPath)

    def setup_profile(self):
        if self.browserBinary :
            self.firefoxBinary = FirefoxBinary(self.browserBinary)
        self.firefoxProfile = webdriver.FirefoxProfile(self.greaseMonkeyProfile)        
        if self.userAgent :
            self.firefoxProfile.set_preference("general.useragent.override",self.userAgent)

    def setup(self):
        self.setup_profile()

        if self.browserBinary :
            self.driver = webdriver.Firefox(firefox_binary = self.firefoxBinary,firefox_profile = self.firefoxProfile)
        else :
            self.driver = webdriver.Firefox(firefox_profile = self.firefoxProfile)
        
        return self.driver



class FireFoxFirebug(WebDriver):
    #the extensions have to be pulled from the extension directory of a version of firefox that is already installed
    fireFoxPath = "/Development/firefox_exe/firefox_35.0/firefox-bin"
    extensionDir = "/Development/firefox_extensions"
    extensions = [#("firebug","firebug@software.joehewitt.com.xpi"),
        #("firebug","firebug-2.0.10-fx.xpi"),
        ("greasemonkey","{e4a8a97b-f2ed-450b-b12d-ee082ba24781}.xpi"),
    ]
    
    def __init__(self):
        WebDriver.__init__(self,browserBinary = self.fireFoxPath)
        
    def load_extensions(self):
        for name,ext_path in self.extensions:
            self.firefoxProfile.add_extension(os.path.join(self.extensionDir,ext_path))
        
    def setup_profile(self):
        if self.browserBinary :
            self.firefoxBinary = FirefoxBinary(self.browserBinary)
        #self.firefoxProfile = webdriver.FirefoxProfile(self.profileDir)
        self.firefoxProfile = webdriver.FirefoxProfile()
        self.load_extensions()
        
        if self.userAgent :
            self.firefoxProfile.set_preference("general.useragent.override",self.userAgent);
    
    def setup(self):
        self.setup_profile()

        if self.browserBinary :
            self.driver = webdriver.Firefox(firefox_binary = self.firefoxBinary,firefox_profile = self.firefoxProfile)
        else :
            self.driver = webdriver.Firefox(firefox_profile = self.firefoxProfile)
        
        return self.driver
