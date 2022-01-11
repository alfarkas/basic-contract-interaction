# stdlib
import json
import os

# deps
import requests
from web3 import exceptions as web3Exceptions

# local
from src.connection import contract, w3
from src.models import Product

from .exceptions import ProductDoesNotExists


def send_transaction(transaction, acc_address):
    """Build a transaction and send it.

    :param transaction: transaction function
    :type transaction: function
    :param acc_address: address to send the transaction from
    :type acc_address: str
    """
    try:
        tx = transaction.buildTransaction(
            {
                "from": acc_address,
                "gas": 210000,
                "gasPrice": w3.eth.gas_price,
                "nonce": w3.eth.get_transaction_count(acc_address),
            }
        )
    except web3Exceptions.InvalidAddress:
        return {"error": "Invalid address"}
    try:
        # call microservice to sign tx
        signed_tx = requests.request(
            "GET",
            os.getenv("SIGN_URL"),
            headers={"content-type": "application/json"},
            json=json.dumps(tx),
        ).json()

        hash_tx = w3.eth.send_raw_transaction(signed_tx["rawTransaction"])
    except Exception as e:
        print(e)
        return {"error": "Something went wrong, try again."}
    return hash_tx


def create_product(name, acc_address):
    """Creates a new product with a given name from an address as owner.

    :param name: name of product
    :type name: str
    :param acc_address: account address
    :type acc_address: str
    :return: hash of the transaction
    :rtype: str
    """
    tx = contract.functions.createProduct(name)
    return send_transaction(tx, acc_address)


def delegate_product(product_id, acc_address, acc2_address):
    """Delegates a product to another account

    :param product_id: id of the product
    :type product_id: int
    :param acc_address: account address that makes the operation
    :type acc_address: str
    :param acc2_address: account address of the new owner
    :type acc2_address: str
    :return: hash of the transaction
    :rtype: str
    """
    tx = contract.functions.delegateProduct(product_id, acc2_address)
    return send_transaction(tx, acc_address)


def accept_product(product_id, acc_address):
    """Accepts a product ownership

    :param product_id: id of the product
    :type product_id: int
    :param acc_address: account address of the new owner
    :type acc_address: str
    :return: hash of the transaction
    :rtype: str
    """
    tx = contract.functions.acceptProduct(product_id)
    return send_transaction(tx, acc_address)


def get_product(product_id):
    """Get a product by id

    :param product_id: product id
    :type product_id: int
    :return: product
    :rtype: list
    """
    try:
        product = contract.functions.products(product_id).call()
    except web3Exceptions.ContractLogicError:
        raise ProductDoesNotExists(product_id)
    return Product(product[0], product[1], product[2], product[3])


def get_products():
    """Get all products

    :return: list of products
    :rtype: list[dict]
    """
    products_amount = contract.functions.size().call()
    products = []
    for i in range(products_amount):
        try:
            products.append(get_product(i).to_dict())
        except ProductDoesNotExists:
            print(f"Unable to get product {i}")
            continue
    return products


def get_product_by_name(name):
    """Get a product by name

    :param name: name of the product to search for
    :param type: str
    :return: product event creation that matches the given name
    :rtype: list[Product]
    """
    products = get_products()
    return list(filter(lambda p: p["name"] == name, products))


def get_delegated_products():
    """Gets products that are currently delegated but not accepted yet.

    :return: list of products delegated
    :rtype: list[Product]
    """
    products = get_products()
    return list(filter(lambda p: p["status"] == 1, products))


def get_delegated_products_by_owner(owner):
    """Filter products by owner

    :param owner: owner to filter by.
    :type owner: str
    :return: products with a given owner.
    :rtype: list[Product]
    """
    products = get_products()
    return list(filter(lambda p: p["owner"] == owner, products))
