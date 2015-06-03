from basepage import BasePage

class RedditPage(BasePage):
    def __init__(self,browser):
        BasePage.__init__(self,brower)

    def get_reddit_title1(self):
        js = """
        var postedItems = Array.prototype.slice.call(document.querySelectorAll("#siteTable div.thing"))

        return postedItems.map(function(postedItem) {
        var aElm = postedItem.querySelector("a.title");
        return [["title",aElm.textContent],
        ["url",aElm.getAttribute("href")],
        ["score",postedItem.querySelector("div.score").textContent]
        ];
        });
        """

        return map(lambda item : dict(item),self.browser.js_execute(js))

    def goto_subreddit(self,subreddit=""):
        self.goto(self,"http://http://www.reddit.com/%s" % subreddit)

