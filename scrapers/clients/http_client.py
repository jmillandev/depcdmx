import requests
import random
import time

class HttpClient:
    HEADERS = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'referrer': 'https://google.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Pragma': 'no-cache',
    }

    def make(self, action, url):
        seconds = random.randint(5, 10)
        print(f"Waiting {seconds} seg to execute: {action.upper()} {url}")
        time.sleep(1)
        return getattr(requests, action)(url, headers=self.HEADERS)
