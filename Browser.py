from selenium.webdriver.chrome.options import Options
from selenium import webdriver

class Browser():
    """
        This class will generate the chrome webdriver for screenshot requests.
    """
    def __init__(self):
        options = Options()
        WEBDRIVER_ARGUMENTS = (
            '--disable-dev-shm-usage',
            '--ignore-certificate-errors',
            '--headless',
            '--incognito',
            '--no-sandbox',
            '--disable-gpu',
            '--disable-extensions',
            '--disk-cache-size=0',
            '--aggressive-cache-discard',
            '--disable-notifications',
            '--disable-remote-fonts',
            '--disable-sync',
            '--window-size=1366,768',
            '--hide-scrollbars',
            '--disable-audio-output',
            '--dns-prefetch-disable',
            '--no-default-browser-check',
            '--disable-background-networking',
            '--enable-features=NetworkService,NetworkServiceInProcess',
            '--disable-background-timer-throttling',
            '--disable-backgrounding-occluded-windows',
            '--disable-breakpad',
            '--disable-client-side-phishing-detection',
            '--disable-component-extensions-with-background-pages',
            '--disable-default-apps',
            '--disable-features=TranslateUI',
            '--disable-hang-monitor',
            '--disable-ipc-flooding-protection',
            '--disable-prompt-on-repost',
            '--disable-renderer-backgrounding',
            '--force-color-profile=srgb',
            '--metrics-recording-only',
            '--no-first-run',
            '--password-store=basic',
            '--use-mock-keychain',
            '--disable-blink-features=AutomationControlled',
            )


        for argument in WEBDRIVER_ARGUMENTS:
            options.add_argument(argument)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        self.driver = webdriver.Chrome(options=options)
        self.driver.set_page_load_timeout(10)

        self.get = self.driver.get
        self.kill = self.driver.quit
        self.screenshot = self.driver.save_screenshot


    def get_title(self, url):
        self.driver.get(url)
        return self.driver.title
