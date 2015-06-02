from basepage import BasePage

class DuckDuckGoPage(BasePage):
    def __init__(self,browser):
        BasePage.__init__(self,brower)

    def search(self,searchTerm):
        self.driver.get("https://duckduckgo.com/")
        inputSearchElm = driver.find_element_by_css_selector('#search_form_input_homepage')
        inputSearchElm.send_keys("%s\n" % searchTerm)

    
