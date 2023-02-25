from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium import webdriver

class Browser():
    """
        This class will generate the chrome webdriver for screenshot requests.
    """
    def __init__(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--window-size=1366,768')
        options.add_argument('--hide-scrollbars',)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        self.driver = webdriver.Chrome(options=options)
        self.driver.set_page_load_timeout(10)

        self.get = self.driver.get
        self.kill = self.driver.quit
        self.screenshot = self.driver.save_screenshot


    def get_title(self, url: str) -> str | None:
        """This function retrieves title from a webpage

        Parameters
        ----------
        url : str
            The url to fetch

        Returns
        -------
        str | None
            The webpage title or none if nothing was found
        """
        try:
            self.driver.get(url)
            return self.driver.title
        except WebDriverException:
            return None
