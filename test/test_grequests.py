import grequests
import time
import requests

urls = [
    'https://jsonplaceholder.typicode.com/todos/1',
    'https://jsonplaceholder.typicode.com/posts/1',
    'https://jsonplaceholder.typicode.com/comments/1',
    'https://jsonplaceholder.typicode.com/photos/1',
    'https://jsonplaceholder.typicode.com/users/1'
]


def exception_handler(request, exception):
    print("Request failed")


def test_exception_handler():
    rs = (grequests.get(u) for u in urls)
    res = grequests.map(rs, exception_handler=exception_handler)
    print(res)


def print_url(r, *args, **kwargs):
    print('hook: ', r.url)


def test_hook():
    url = "http://www.baidu.com"
    res = requests.get(url, hooks={"response": print_url})
    print(res)

    tasks = []
    req = grequests.get(url, callback=print_url)
    tasks.append(req)
    res = grequests.map(tasks)
    print(res)


def method1():
    t1 = time.time()
    for url in urls:
        res = requests.get(url)
        # print res.status_code

    t2 = time.time()
    print('method1', t2 - t1)


def method2():
    tasks = [grequests.get(u) for u in urls]
    t1 = time.time()
    res = grequests.map(tasks, size=3)
    #    print res
    t2 = time.time()
    print('method2', t2 - t1)


def method3():
    tasks = [grequests.get(u) for u in urls]
    t1 = time.time()
    res = grequests.map(tasks, size=6)
    #    print res
    t2 = time.time()
    print('method3', t2 - t1)


# method1()
# method2()
# method3()
# method1 8.312755584716797
# method2 2.2688870429992676
# method3 1.581711769104004

test_hook()
