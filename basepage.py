class BasePage(object):
    url = None

    def __init__(self,browser):
        self.browser = browser
        self.driver = browser.driver
        #make nice shortcuts to browser
        self.js_ex = self.browser.js_ex
        
    def find_elements_with_text(self,tagName,rePattern):
        return self.driver.execute_script("""
        return (function(tag,pattern) {
        var patt = RegExp(pattern);
        var elms = Array.prototype.slice.call(document.getElementsByTagName(tag));
        return elms.filter(function(elm) {
        return patt.test(elm.textContent);
        })
        })(arguments[0],arguments[1]);
        """,tagName,rePattern)

    def scroll_top(self):
        self.driver.execute_script("window.scrollTo(0,0);")
        return True

    def scroll_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        return True

    def goto(self,url = None):
        if url :
            self.driver.get(url)
        else:
            self.driver.get(self.url)

    def ipython_screenshot(self):
        from IPython.display import Image
        img = self.driver.get_screenshot_as_png()
        return Image(data = img)
