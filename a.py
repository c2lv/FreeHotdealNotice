import requests
import time

def random_proxy(url, params={}):
    if params:
        url += '?'
        for key, value in params.items():
            url += f'{key}={value}&'
    response = requests.get(url)
    return response

for i in range(1, 10):
    begin = time.time()
    response = random_proxy('https://www.dongguk.edu/article/IPSINOTICE/list', {'pageIndex': i})
    end = time.time()
    result = end - begin
    result = round(result, 3)
    print("time taken to execute random_proxy(): ", result)