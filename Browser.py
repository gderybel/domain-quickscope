from selenium.webdriver.chrome.options import Options
from selenium import webdriver

class Browser():
    """
        This class will generate the chrome webdriver for screenshot requests.
    """
    def __init__(self):
        options = Options()
        options.add_argument('--headless')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        self.driver = webdriver.Chrome(options=options)
        self.driver.set_page_load_timeout(10)

        self.get = self.driver.get
        self.kill = self.driver.quit
        self.screenshot = self.driver.save_screenshot


    def get_title(self, url):
        self.driver.get(url)
        return self.driver.title
