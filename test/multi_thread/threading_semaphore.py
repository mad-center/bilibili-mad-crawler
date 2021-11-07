from time import sleep
import threading

# Number of parallel threads
lock = threading.Semaphore(2)


# https://stackoverflow.com/a/38671899

def parse(url):
    """
    Change to your logic, I just use sleep to mock http request.
    """

    print('getting info', url)
    sleep(2)

    # After we done, subtract 1 from the lock
    lock.release()


def parse_pool():
    # List of all your urls
    list_of_urls = ['website1', 'website2', 'website3', 'website4']

    # List of threads objects I so we can handle them later
    thread_pool = []

    for url in list_of_urls:
        # Create new thread that calls to your function with a url
        thread = threading.Thread(target=parse, args=(url,))
        thread_pool.append(thread)
        thread.start()

        # Add one to our lock, so we will wait if needed.
        # If it is zero on entry, block, waiting until some other thread has called release() to make it larger than zero.
        lock.acquire()

    for thread in thread_pool:
        thread.join()

    print('done')

parse_pool()