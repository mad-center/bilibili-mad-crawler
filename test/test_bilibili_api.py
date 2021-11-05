import requests

# url concatenation
path = 'https://api.bilibili.com/x/web-interface/newlist'
rid = 24
type = 0
pn = 1
ps = 20
url = f'{path}?rid={rid}&type={type}&pn={pn}&ps={ps}'
print(url)


def test_proxy():
    http_proxy = "http://123.56.89.115:7890"
    https_proxy = "https://123.56.89.115:7890"

    proxies = {
        "http": http_proxy,
        "https": https_proxy,
    }

    r = requests.get(url, proxies=proxies)
    print(r.text)


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
    test_fetch_page()
