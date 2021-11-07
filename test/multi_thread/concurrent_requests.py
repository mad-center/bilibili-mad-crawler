from concurrent import futures
import requests


def request_post(url, data):
    return requests.post(url, data=data)


with futures.ThreadPoolExecutor(max_workers=3) as executor:
    payload = dict(key1='value1', key2='value2')
    url = 'https://httpbin.org/post'
    res = [executor.submit(request_post, url, payload) for _ in range(3)]
    futures.wait(res)
    for response in res:
        result = response.result()
        print(result.status_code)
