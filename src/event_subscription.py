# stdlib
import asyncio

# deps
from web3 import exceptions as web3Exceptions

# local
from src.connection import *


class WatchList:
    _subscribers = []

    def get_subscribers(self):
        return self._subscribers.copy()

    def subscribe(self, address):
        """Add an address to the subscriber list

        :param address: wallet address to add
        :type address: str
        """
        self._subscribers.append(address)

    def unsubscribe(self, address):
        """Removes an address to the subscriber list.

        :param address: wallet address to remove from the subscribers
        :type address: str
        """
        self._subscribers.remove(address)

    def is_subscribed(self, address):
        """Returns a boolean indicating if the given address is in the subscription list or not.

        :param address: address to check
        :type address: str
        """
        return address in self._subscribers


def is_transaction_successfull(tx_hash):
    """Checks if the transaction is in the blockchain and if its status is success.

    :param tx_hash: hash of the transaction
    :type tx_hash: str
    :return: transaction successfull or not
    :rtype: boolean
    """
    try:
        transaction = w3.eth.get_transaction_receipt(tx_hash)
    except web3Exceptions.TransactionNotFound:
        transaction = None

    return False if not transaction else transaction["status"] == 1


def has_min_confirmations(transaction_block_number, tx_hash):
    """Checks if the given transaction was successful and if a minimum amount of blocks have been
    process since the transaction took place.

    :param transaction_block_number: block in which the transaction took place.
    :type transaction_block_number: str
    :param tx_hash: hash of the transaction
    :type tx_hash: str
    :return: True or False, if the transaction was successful and the minimum amount of blocks has been processed.
    :rtype: boolean
    """
    return w3.eth.block_number - transaction_block_number >= int(
        os.environ["MINIMUM_CONFIRMATION"]
    ) and is_transaction_successfull(tx_hash)


async def handle_event(event):
    wl = WatchList()
    if event.event != "DelegateProduct" or wl.is_subscribed(event.args.newOwner):
        # check every 3 seconds if it has the minimum confirmations
        while not has_min_confirmations(event.blockNumber, event.transactionHash):
            await asyncio.sleep(3)
    print(Web3.toJSON(event))


async def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            asyncio.create_task(handle_event(event))
        await asyncio.sleep(poll_interval)


def polling_new_products():
    event_filter = contract.events.NewProduct.createFilter(fromBlock="latest")
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(log_loop(event_filter, 2)))
    finally:
        # close loop to free up system resources
        loop.close()


def polling_delegated_products():
    event_filter = contract.events.DelegateProduct.createFilter(fromBlock="latest")
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(log_loop(event_filter, 2)))
    finally:
        # close loop to free up system resources
        loop.close()


def polling_accepted_products():
    event_filter = contract.events.AcceptProduct.createFilter(fromBlock="latest")
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(log_loop(event_filter, 2)))
    finally:
        # close loop to free up system resources
        loop.close()
