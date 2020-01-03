import json
import requests
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

from FPLManager import settings
from .utils import top_50_url, stats_url

class FplStatistics:

    PRICE_CHANGE_URL = 'http://www.fplstatistics.co.uk/'

    def __init__(self):
        self.session = requests.Session()
        self.driver = self.initialise_selenium()
        self.price_data_url = self.get_price_data_url()
        self.player_price_data = self.get_player_price_data()
        self.top_50_data = self.get_top_50_data()
        self.player_stats_data = self.get_player_stats_data()
        

    @staticmethod
    def initialise_selenium():
        caps = DesiredCapabilities.CHROME
        
        if settings.is_prod:
            caps['goog:loggingPrefs'] = {'performance': 'ALL'}
        else:
            caps['loggingPrefs'] = {'performance': 'ALL'}

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        d = webdriver.Chrome(options=chrome_options,
                             desired_capabilities=caps)
        return d

    def get_price_data_url(self):
        self.driver.get(self.PRICE_CHANGE_URL)
        browser_log = self.driver.get_log('performance')
        all_events = [json.loads(entry['message'])['message'] for entry in browser_log]
        response_events = [event for event in all_events if 'Network.response' in event['method']]
        
        for event in response_events:
            if 'response' in event['params']:
                if 'http://www.fplstatistics.co.uk/Home/AjaxPrices' in event['params']['response']['url']:
                    return event['params']['response']['url']

    def get_player_price_data(self):
        return json.loads(self.session.get(self.price_data_url).text)['aaData']

    def get_top_50_data(self):
        return json.loads(self.session.get(top_50_url).text)['aaData']

    def get_player_stats_data(self):
        return json.loads(self.session.get(stats_url).text)['aaData']

if __name__ == '__main__':
    d = FplStatistics()
    r = 0