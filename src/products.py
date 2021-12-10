from src.connection import *

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
    # TODO update to new format (dynamic)
    tx = contract.functions.createProduct(name).buildTransaction(
        {
            "from": acc_address,
            "gas": 210000,
            "gasPrice": w3.eth.gas_price,
            "nonce": w3.eth.get_transaction_count(acc_address)
        }
    )
    signed_tx = w3.eth.account.sign_transaction(tx, key)

    hash_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return hash_tx

def delegate_product(product_id, acc_address, key):
    """Delegates a product to another account

    :param product_id: id of the product
    :type product_id: int
    :param acc_address: account address that makes the operation
    :type acc_address: str
    :param key: private key of the account
    :type key: str
    :return: hash of the transaction
    :rtype: str
    """
    tx = contract.functions.delegateProduct(product_id, acc_address).buildTransaction(
        {
            "from": acc_address,
            "gas": 210000,
            "gasPrice": w3.eth.gas_price,
            "nonce": w3.eth.get_transaction_count(acc_address)
        }
    )
    signed_tx = w3.eth.account.sign_transaction(tx, key)

    hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return hash

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
    tx = contract.functions.acceptProduct(product_id).buildTransaction(
        {
            "from": acc_address,
            "gas": 210000,
            "gasPrice": w3.eth.gas_price,
            "nonce": w3.eth.get_transaction_count(acc_address)
        }
    )
    signed_tx = w3.eth.account.sign_transaction(tx, key)

    hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return hash

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

    :return: list of product creations
    :rtype: list[dict]
    """
    event_filter_new = contract.events.NewProduct.createFilter(fromBlock=created_block) 
    return event_filter_new.get_all_entries()

def get_product_by_name(name):
    """Get a product by name
    
    :param name: name of the product to search for
    :param type: str
    :return: product event creation that matches the given name
    :rtype: list[dict]
    """
    event_filter_new = contract.events.NewProduct.createFilter(fromBlock=created_block, argument_filters={"name": name}) 
    return event_filter_new.get_all_entries()
