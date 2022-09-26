from const import *
import requests

def random_proxy(url, params={}):
    if params:
        url += '?'
        for key, value in params.items():
            url += f'{key}={value}&'
    payload = {
        "api_key": SCRAPER_API_KEY,
        "url": url,
    }
    response = requests.get("http://api.scraperapi.com", params = payload)
    return response

# Remove tab and right space
def remove_tab(str):
    return str.replace('\t', '').rstrip()