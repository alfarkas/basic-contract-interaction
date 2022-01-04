# local
from app import app, delegate
from src.products import (
    create_product,
    delegate_product,
    get_product,
    get_products,
)
from src.tests.fixtures import *


client = app.test_client()


def test_create_product(mock_contract, mock_w3, account_1):
    all_products = get_products()
    assert len(all_products) == 0

    response = client.post(
        "/product/",
        data={
            "name": "test_product",
            "address": account_1.address,
            "key": account_1.key.hex(),
        },
    )

    assert response.status_code == 200
    # returns a valid transaction hash
    assert response.get_json()["transaction_hash"].startswith("0x")

    all_products = get_products()
    assert len(all_products) == 1
    assert all_products[0][0] == "test_product"


def test_create_product_invalid_address(mock_contract, mock_w3, account_1):
    response = client.post(
        "/product/",
        data={
            "name": "test_product",
            "address": "0",
            "key": account_1.key.hex(),
        },
    )
    assert response.status_code == 200
    assert response.get_json() == {"transaction_hash": {"error": "Invalid address"}}


def test_create_product_invalid_key(mock_contract, mock_w3, account_1):
    response = client.post(
        "/product/",
        data={
            "name": "test_product",
            "address": account_1.address,
            "key": "0",
        },
    )
    assert response.status_code == 200
    assert response.get_json() == {
        "transaction_hash": {"error": "Something went wrong, try again."}
    }


def test_read_product(mock_contract, mock_w3, account_1):
    create_product("test_product_0", account_1.address, account_1.key)

    response = client.get("/product/0")
    assert response.status_code == 200
    assert response.get_json() == {
        "product": [
            "test_product_0",
            0,
            account_1.address,
            "0x0000000000000000000000000000000000000000",
        ]
    }


def test_read_product_raise_exception(mock_contract, mock_w3, mock_exception):
    response = client.get("/product/0")
    assert response.status_code == 200
    assert response.get_json() == {"error": "Product 0 does not exists."}


def test_read_products(mock_contract, mock_w3, account_1):
    create_product("test_product_0", account_1.address, account_1.key)
    create_product("test_product_1", account_1.address, account_1.key)

    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json() == {
        "products": [
            [
                "test_product_0",
                0,
                account_1.address,
                "0x0000000000000000000000000000000000000000",
            ],
            [
                "test_product_1",
                0,
                account_1.address,
                "0x0000000000000000000000000000000000000000",
            ],
        ]
    }


def test_delegate_product(
    product_contract, mock_contract, mock_w3, account_1, account_2, new_product
):
    response = client.post(
        "/product/0/delegate/",
        data={
            "address": account_1.address,
            "key": account_1.key.hex(),
            "new_address": account_2.address,
        },
    )
    assert response.status_code == 200
    # returns a valid transaction hash
    assert response.get_json()["transaction_hash"].startswith("0x")

    product = get_product(0)
    assert product[0] == "new_prod"
    assert product[1] == 1
    assert product[3] == account_2.address


def test_delegate_product_invalid_address(
    product_contract, mock_contract, mock_w3, account_1, account_2, new_product
):
    response = client.post(
        "/product/0/delegate/",
        data={
            "address": "0",
            "key": account_1.key.hex(),
            "new_address": account_2.address,
        },
    )
    assert response.status_code == 200
    assert response.get_json() == {"transaction_hash": {"error": "Invalid address"}}


def test_delegate_product_invalid_key(
    product_contract, mock_contract, mock_w3, account_1, account_2, new_product
):

    response = client.post(
        "/product/0/delegate/",
        data={
            "address": account_1.address,
            "key": "0",
            "new_address": account_2.address,
        },
    )
    assert response.status_code == 200
    assert response.get_json() == {
        "transaction_hash": {"error": "Something went wrong, try again."}
    }


def test_delegate_product_invalid_new_address(
    product_contract, mock_contract, mock_w3, account_1, account_2, new_product
):

    response = client.post(
        "/product/0/delegate/",
        data={
            "address": account_1.address,
            "key": account_1.key.hex(),
            "new_address": "0",
        },
    )
    assert response.status_code == 200
    assert response.get_json() == {
        "transaction_hash": {"error": "Something went wrong, try again."}
    }


def test_accept_product(mock_contract, mock_w3, account_1, account_2):
    create_product("test_product_0", account_1.address, account_1.key)
    delegate_product(0, account_1.address, account_1.key, account_2.address)

    response = client.post(
        "/product/0/accept/",
        data={
            "address": account_2.address,
            "key": account_2.key.hex(),
        },
    )
    assert response.status_code == 200
    # returns a valid transaction hash
    assert response.get_json()["transaction_hash"].startswith("0x")

    product = get_product(0)
    assert product[1] == 0
    assert product[2] == account_2.address


def test_accept_product_invalid_address(mock_contract, mock_w3, account_1, account_2, new_product):
    delegate_product(0, account_1.address, account_1.key, account_2.address)

    response = client.post(
        "/product/0/accept/",
        data={
            "address": "0",
            "key": account_2.key.hex(),
        },
    )
    assert response.status_code == 200
    assert response.get_json() == {"transaction_hash": {"error": "Invalid address"}}


def test_accept_product_invalid_key(mock_contract, mock_w3, account_1, account_2):
    create_product("test_product_0", account_1.address, account_1.key)
    delegate_product(0, account_1.address, account_1.key, account_2.address)

    response = client.post(
        "/product/0/accept/",
        data={
            "address": account_2.address,
            "key": "0",
        },
    )
    assert response.status_code == 200
    assert response.get_json() == {
        "transaction_hash": {"error": "Something went wrong, try again."}
    }
