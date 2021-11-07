import json
import requests


# !remember to set local proxy: bypass these urls

def test_get():
    r = requests.get('https://example.com')
    print(r.text)
    print(r.content.decode())


def test_post():
    payload = dict(key1='value1', key2='value2')
    r = requests.post('https://httpbin.org/post', data=payload)
    print(r.text)


def test_other_methods():
    r = requests.put('https://httpbin.org/put', data={'key': 'value'})
    r = requests.delete('https://httpbin.org/delete')
    r = requests.head('https://httpbin.org/get')
    r = requests.options('https://httpbin.org/get')


def test_headers():
    url = 'https://api.github.com/some/endpoint'
    headers = {'user-agent': 'my-app/0.0.1'}
    r = requests.get(url, headers=headers)
    print(r.text)


def test_json():
    url = 'https://api.github.com/some/endpoint'
    payload = {'some': 'data'}
    r = requests.post(url, json=payload)
    print(r.text)


def test_use_proxies():
    proxies = {'http': '127.0.0.1:7890', 'https': '127.0.0.1:7890'}
    r = requests.get('http://baidu.com', proxies=proxies)
    print(r.text)
    r = requests.get('https://baidu.com', proxies=proxies)
    print(r.text)


def test_use_session():
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.28 Safari/537.36'
    }

    s = requests.Session()
    s.headers = headers
    proxies = {'https': '127.0.0.1:7890'}
    r = s.get('https://baidu.com/', proxies=proxies)
    print(r.status_code)
    print(s.headers)

    s.close()


def test_local_proxy_to_bilibili():
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.28 Safari/537.36'
    }

    s = requests.Session()
    proxies = {'https': '127.0.0.1:7890'}
    r = s.get('https://api.bilibili.com/', proxies=proxies)
    print(r.status_code)
    print(s.headers)
    # {'User-Agent': 'python-requests/2.25.1', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}

    s.headers = headers
    r = s.get('https://api.bilibili.com/', proxies=proxies)
    print(r.status_code)
    print(s.headers)
    # {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.28 Safari/537.36'}

    s.close()


def test_other_proxy_to_bilibili():
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.28 Safari/537.36'
    }

    s = requests.Session()
    s.headers = headers
    proxies = {'https': '124.156.147.244:59394'}
    r = s.get('https://api.bilibili.com/', proxies=proxies)
    print(r.status_code)
    print(s.headers)

    s.close()


def test_set_cookie():
    s = requests.Session()

    s.get('http://httpbin.org/cookies/set/sessioncookie/123456789')
    r = s.get("http://httpbin.org/cookies")

    print(r.text)
    # '{"cookies": {"sessioncookie": "123456789"}}'


# test_get()
# test_post()
# test_headers()
# test_other_methods()
# test_json()
# test_use_proxies()
# test_use_session()
# test_set_cookie()
# test_local_proxy_to_bilibili()
test_other_proxy_to_bilibili()
