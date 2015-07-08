import util,urlparse,sys,os.path
from selenium.common.exceptions import ElementNotVisibleException,StaleElementReferenceException,WebDriverException
import copy,ipython_helpers

"""
basepage.py
for all reddit pages
"""

class HtmlAttribute(object):
    pass

class HtmlElement(object):
    def __init__(self,description):
        """
        description is a list of dicts describing the element 
        """
        self._description = dict(description)
        self._attributes = HtmlAttribute()
        for attribute,value in self._description["attributes"] :
            attribute = attribute.replace("-","_")
            setattr(self._attributes,attribute,value)
            
    def __repr__(self):
        fmt = 'HtmlElement at 0x%x atag : "%s" id : "%s" class : "%s"' 
        return fmt % (hash(self),
                      self.tag,
                      getattr(self._attributes,"id",""),
                      getattr(self._attributes,"class",""))
    
    @property
    def tag(self):
        return self._description["tag"]
    
    @property
    def attributes(self):
        return self._attributes
    
    def display(self):
        import ipython_helpers
        attributes = dict(self._description["attributes"])
        startKeys = ["tag","id","class"]
        allKeys = copy.copy(startKeys)
        allKeys.extend(filter(lambda k: startKeys.count(k) == 0,attributes.keys()))
        attributes["tag"] = self.tag
        attributes["id"] = getattr(self._attributes,"id","")
        attributes["class"] = getattr(self._attributes,"class","")
        return ipython_helpers.dict_to_html(attributes,keys = allKeys)

class WebEvent(object):
    def __init__(self,descriptionList):
        self.descriptionList = descriptionList
        self.htmlElements = []
        
        for description in descriptionList :
            self.htmlElements.append(HtmlElement(description))
    
    def __repr__(self):
        fmt = 'WebEvent at 0x%x %s'
        results = []
        results.append("[")
        for elm in self.htmlElements:
            results.append(repr(elm))
        results.append("]")
        htmlElementsStr = "\n".join(results)
        return fmt % (hash(self),htmlElementsStr)
    
    def display(self):
        from IPython.display import HTML
        results = []
        for elm in self.htmlElements:
            results.append(elm.display().data)
        return HTML("\n".join(results))

class BasePage(object):
    """
    //imgResult.querySelector("div.rg_anbg").textContent
    html = document.querySelector("html") //.getAttribute("webdriver")
    html.removeAttribute("webdriver")
    webdriver firefox tags
    http://stackoverflow.com/questions/22711441/remove-readonly-attributes-in-selenium-webdriver?answertab=active#tab-top

    this is where it is being set
    https://searchcode.com/codesearch/view/30471386/
    docElement.setAttribute('webdriver', 'true')
    ~/.mozilla/firefox/3u4a90pf.default/gm_scripts$
    #grease monkey scripts are enabled at config.xml
    http://gruntjs.com/getting-started
    """
    url = None
    js_dict_to_array = """
    window.dict_to_array = function(dict) {
        var result = [];
        for(var k in dict) {
            result.push([k,dict[k]]);
        }
        return result;}
    """
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

    def find_css(self,css):
        elm = self.driver.find_element_by_css_selector(css)
        return elm
        
    def find_css_input(self,css,value):
        elm = self.driver.find_element_by_css_selector(css)
        elm.clear()
        elm.send_keys(value)
        return elm
    
    def find_css_click(self,css):
        try :
            elm = self.driver.find_element_by_css_selector(css)
            elm.click()
            return elm
        except ElementNotVisibleException:
            return None

    def get_module_dir(self):        
        thismodule = sys.modules[__name__]
        return os.path.split(os.path.abspath(os.path.abspath(thismodule.__file__)))[0]

    def load_js(self,filename):
        with open(os.path.join(self.get_module_dir(),filename),"r") as f:
            js = f.read()
            self.driver.execute_script(js)
        return True

    def load_recorder(self,addStyleSheet = True):
        cssSheet = """
        .js_active {
        outline-width: 1px;
        outline-style: dashed;
        outline-color: red;
        background-color: red;
        background: red;
        }
        """
        self.load_js("recorder.js")
        if addStyleSheet :
            self.driver.execute_script("return window._$recorder.add_style_sheet()")
            self.edit_style_sheet(cssSheet);

    def edit_style_sheet(self,styleString):
        self.driver.execute_script("window._$recorder.edit_style_string(arguments[0])",styleString)

    def start_recorder(self):
        self.driver.execute_script("return window._$recorder.start();")

    def stop_recorder(self):
        return self.driver.execute_script("return window._$recorder.stop();")

    def get_recorder_events(self):
        jsEvents = self.driver.execute_script("return window._$recorder.click_events;")
        events = map(lambda event: WebEvent(event),jsEvents)
        return events

    def clear_recorder_events(self):
        self.driver.execute_script("window._$recorder.click_events = [];");

    def get_last_event(self):
        return self.get_recorder_events()[-1]

    def highlight_css_selected(self,cssSelector):
        self.driver.execute_script("window._$recorder.highlight_css_selected(arguments[0]);",cssSelector)

    def unhighlight_css_selected(self):
        self.driver.execute_script("window._$recorder.unhighlight_css_selected();")

    def display_events(self,events = None):
        from IPython.display import HTML
        if not(events):
            events = self.get_recorder_events()
        rows = apply(zip,map(lambda e: e.htmlElements,events))
        table = ["<table>"]
        for row in rows :
            table.append("<tr>")
            for elm in row :
                table.append("<td>")
                table.append("<dl>")
                table.append("<dt>tag</dt><dd>%s</dd>" % elm.tag)
                table.append("<dt>id</dt><dd>%s</dd>" % getattr(elm.attributes,"id",""))
                table.append("<dt>class</dt><dd>%s</dd>" % getattr(elm.attributes,"class",""))
                table.append("</dl>")
                table.append("</td>")
            table.append("</tr>")
        table.append("</table>")        
        return HTML("".join(table))

