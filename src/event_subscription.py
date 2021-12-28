import asyncio
from src.connection import *


def handle_event(event):
    print(Web3.toJSON(event))


async def log_loop(event_filter, poll_interval):
    while True:
        for product_created in event_filter.get_new_entries():
            handle_event(product_created)
        await asyncio.sleep(poll_interval)


def polling_new_products():
    event_filter = contract.events.NewProduct.createFilter(fromBlock="latest")
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncio.gather(log_loop(event_filter, 2)))
    finally:
        # close loop to free up system resources
        loop.close()
