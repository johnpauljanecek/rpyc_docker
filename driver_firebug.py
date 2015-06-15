from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from rpyc_docker.drivers import WebDriver

class FireFoxFirebug(WebDriver):
    fireFoxPath = "/Development/firefox_exe/firefox_35.0/firefox-bin"
    extensionDir = "/Development/firefox_extensions"
    extensions = [("firebug","firebug@software.joehewitt.com.xpi"),
                    ("greasemonkey","greasemonkey-3.2-fx.xpi"),
                     ]
    
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
            self.driver = webdriver.Firefox(firefox_binary = self.firefoxBinary,firefox_profile = self.firefoxProfile)
        else :
            self.driver = webdriver.Firefox(firefox_profile = self.firefoxProfile)
        
        return self.driver
