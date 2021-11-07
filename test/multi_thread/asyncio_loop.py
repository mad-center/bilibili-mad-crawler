from time import sleep

import asyncio


# https://stackoverflow.com/a/38672388

async def parse(url):
    print('in parse for url {}'.format(url))

    sleep(2)
    info = 'mock response'  # write the logic for fetching the info, it waits for the responses from the urls

    print('done with url {}'.format(url))
    return 'parse {} result from {}'.format(info, url)


async def main(sites):
    print('starting main')
    parses = [parse(url) for url in sites]
    print('waiting for phases to complete')
    completed, pending = await asyncio.wait(parses)

    results = [t.result() for t in completed]
    print('results: {}'.format(results))


event_loop = asyncio.get_event_loop()
try:
    websites = ['site1', 'site2', 'site3']
    event_loop.run_until_complete(main(websites))
finally:
    event_loop.close()
