import json
import requests

# get
# r = requests.get('https://hello.world')
# print(r.text)
# print(r.content.decode())

# post
# payload = dict(key1='value1', key2='value2')
# r = requests.post('https://httpbin.org/post', data=payload)
# print(r.text)

# r = requests.put('https://httpbin.org/put', data={'key': 'value'})
# r = requests.delete('https://httpbin.org/delete')
# r = requests.head('https://httpbin.org/get')
# r = requests.options('https://httpbin.org/get')

# headers
# url = 'https://api.github.com/some/endpoint'
# headers = {'user-agent': 'my-app/0.0.1'}
# r = requests.get(url, headers=headers)
# print(r.text)

# json
# url = 'https://api.github.com/some/endpoint'
# payload = {'some': 'data'}
# r = requests.post(url, json=payload)
# print(r.text)

# cookie
# url = 'http://example.com/some/cookie/setting/url'
# r = requests.get(url)
# print(r.cookies['example_cookie_name'])
