from src.connection import *


def send_transaction(transaction, acc_address, key):
    """Build a transaction and send it.

    :param transaction: transaction function
    :type transaction: function
    :param acc_address: address to send the transaction from
    :type acc_address: str
    :param key: private key from the address
    :type key: str
    """
    tx = transaction.buildTransaction(
        {
            "from": acc_address,
            "gas": 210000,
            "gasPrice": w3.eth.gas_price,
            "nonce": w3.eth.get_transaction_count(acc_address),
        }
    )
    signed_tx = w3.eth.account.sign_transaction(tx, key)

    hash_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return hash_tx


def create_product(name, acc_address, key):
    """Creates a new product with a given name from an address as owner.

    :param name: name of product
    :type name: str
    :param acc_address: account address
    :type acc_address: str
    :param key: private key of the account
    :type key: str
    :return: hash of the transaction
    :rtype: str
    """
    tx = contract.functions.createProduct(name)
    return send_transaction(tx, acc_address, key)


def delegate_product(product_id, acc_address, key, acc2_address):
    """Delegates a product to another account

    :param product_id: id of the product
    :type product_id: int
    :param acc_address: account address that makes the operation
    :type acc_address: str
    :param key: private key of the account
    :type key: str
    :param acc2_address: account address of the new owner
    :type acc2_address: str
    :return: hash of the transaction
    :rtype: str
    """
    tx = contract.functions.delegateProduct(product_id, acc2_address)
    return send_transaction(tx, acc_address, key)


def accept_product(product_id, acc_address, key):
    """Accepts a product ownership

    :param product_id: id of the product
    :type product_id: int
    :param acc_address: account address of the new owner
    :type acc_address: str
    :param key: private key of the account
    :type key: str
    :return: hash of the transaction
    :rtype: str
    """
    tx = contract.functions.acceptProduct(product_id)
    return send_transaction(tx, acc_address, key)


def get_product(product_id):
    """Get a product by id

    :param product_id: product id
    :type product_id: int
    :return: product
    :rtype: list
    """
    return contract.functions.products(product_id).call()


def get_products():
    """Get all products

    :return: list of products
    :rtype: list
    """
    products_amount = contract.functions.size().call()
    products = [get_product(i) for i in range(products_amount)]
    return products


def get_product_by_name(name):
    """Get a product by name

    :param name: name of the product to search for
    :param type: str
    :return: product event creation that matches the given name
    :rtype: list[dict]
    """
    event_filter_name = contract.events.NewProduct.createFilter(
        fromBlock=created_block, argument_filters={"name": name}
    )
    return event_filter_name.get_all_entries()


def get_delegated_products():
    """Gets products that are currently delegated but not accepted yet.

    :return: list of products delegated
    :rtype: list[AttributedDict]
    """
    delegated_product_event_filter = contract.events.DelegateProduct.createFilter(
        fromBlock=created_block
    )
    delegated_products = delegated_product_event_filter.get_all_entries()

    accepted_product_event_filter = contract.events.AcceptProduct.createFilter(
        fromBlock=created_block
    )
    accepted_products = accepted_product_event_filter.get_all_entries()
    accepted_prod_ids = [p["args"]["productId"] for p in accepted_products]

    currently_delegated = [
        p for p in delegated_products if p["args"]["productId"] not in accepted_prod_ids
    ]

    return currently_delegated


def get_accepted_products():
    """Get all accepted product delegations.

    :return: list of products accepted
    :rtype: list[AttributedDict]
    """
    accepted_product_event_filter = contract.events.AcceptProduct.createFilter(
        fromBlock=created_block
    )
    return accepted_product_event_filter.get_all_entries()


def get_delegated_products_by_owner(owner):
    """Filter delegated products by owner

    :param owner: owner to filter by.
    :type owner: str
    :return: products delegated to the given owner.
    :rtype: list[AttributedDict]
    """
    delegated_product_event_filter_owner = contract.events.DelegateProduct.createFilter(
        fromBlock=created_block, argument_filters={"newOwner": owner}
    )
    return delegated_product_event_filter_owner.get_all_entries()
