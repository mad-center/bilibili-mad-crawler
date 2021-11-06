import requests

# url concatenation
path = 'https://api.bilibili.com/x/web-interface/newlist'
rid = 24
type = 0
pn = 1
ps = 20
url = f'{path}?rid={rid}&type={type}&pn={pn}&ps={ps}'
# print(url)


def test_proxy():
    # clash local proxy
    http_proxy = "http://127.0.0.1:7890"
    https_proxy = "https://127.0.0.1:7890"

    proxies = {
        "http": http_proxy,
        "https": https_proxy,
    }

    url1 = 'https://api.bilibili.com'
    url2 = 'https://youtube.com'
    url3 = 'https://baidu.com'
    try:
        r1 = requests.get(url1, proxies=proxies)
        print(r1.text)
    except Exception as e:
        print(e)

    try:
        r2 = requests.get(url2, proxies=proxies)
        print(r2.text)
    except Exception as e:
        print(e)

    try:
        r3 = requests.get(url3, proxies=proxies)
        print(r3.text)
    except Exception as e:
        print(e)


def test_fetch_page():
    try:
        r = requests.get(url)
        json = r.json()
        if json and json['code'] == 0:
            print(len(json["data"]["archives"]))
        else:
            print('response ok but no data')
    except Exception as e:
        # HTTPSConnectionPool(host='api.bilibili.com', port=443):
        # Max retries exceeded with url: /x/web-interface/newlist?rid=24&type=0&pn=1&ps=20
        # (Caused by ProxyError('Cannot connect to proxy.', OSError(0, 'Error')))
        print(e)


if __name__ == '__main__':
    test_proxy()
