from concurrent import futures

proxies = []


def is_proxy_alive(proxy):
    return False


with futures.ThreadPoolExecutor(max_workers=5) as executor:
    future_proxy_mapping = {}
    futures = []
    for proxy in proxies:
        future = executor.submit(is_proxy_alive, proxy)
        futures.append(future)
        future_proxy_mapping[future] = proxy

    for future in futures:
        proxy = future_proxy_mapping[future]
        print(proxy)
        print(future.result())
