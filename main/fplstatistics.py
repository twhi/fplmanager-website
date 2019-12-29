from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options


class FplStatistics:

    PRICE_CHANGE_URL = 'http://www.fplstatistics.co.uk/'

    def __init__(self):
        self.driver = self.initialise_selenium()

    @staticmethod
    def initialise_selenium():
        caps = DesiredCapabilities.CHROME
        caps['loggingPrefs'] = {'performance': 'ALL'}
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        d = webdriver.Chrome(options=chrome_options,
                             desired_capabilities=caps)
        return d

if __name__ == '__main__':
    FplStatistics()