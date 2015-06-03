from basepage import BasePage
import time

class DuckDuckGoPage(BasePage):
    def __init__(self,browser):
        BasePage.__init__(self,browser)

    def load_all_results(self):
        self.resultElms = self.driver.find_elements_by_css_selector("#links>div.results_links_deep")
        while True :
            self.scroll_bottom()
            time.sleep(4)
            newResultElms = self.driver.find_elements_by_css_selector("#links>div.results_links_deep")
            if len(newResultElms) == len(self.resultElms):
                self.resultElms = newResultElms
                break
            self.resultElms = newResultElms    

    def search(self,searchTerm):
        self.driver.get("https://duckduckgo.com/")
        inputSearchElm = self.driver.find_element_by_css_selector('#search_form_input_homepage')
        inputSearchElm.send_keys("%s\n" % searchTerm)
        self.load_all_results()

    
    def get_results(self):
        jsFunction = """
        var resultElms = Array.prototype.slice.call(document.querySelectorAll("#links>div.results_links_deep"))
        return resultElms.map(function(resultElm) {
            var result = [];
            var resultAElm = resultElm.querySelector("a.result__a");
            result.push(["title",resultAElm.textContent]);
            result.push(["href",resultAElm.getAttribute("href")]);
            result.push(["snippet",resultElm.querySelector("div.result__snippet").textContent]);
            return result;
            });
        """
        results = self.driver.execute_script(jsFunction)
        return map(dict,results)
