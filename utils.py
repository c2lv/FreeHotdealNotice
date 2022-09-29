from const import *
import requests

def get_requests(url, params={}):
    if params:
        url += '?'
        for key, value in params.items():
            url += f'{key}={value}&'
    response = requests.get(url)
    return response

# Remove tab and right space
def remove_tab(str):
    return str.replace('\t', '').rstrip()