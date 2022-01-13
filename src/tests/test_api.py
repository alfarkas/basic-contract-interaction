# local
from unittest.mock import MagicMock, patch
from app import app, delegate
from src.exceptions import ProductDoesNotExists
from src.products import (
    create_product,
    delegate_product,
    get_product,
    get_products,
)
from src.tests.fixtures import *
from hexbytes import HexBytes

client = app.test_client()

@patch("app.create_product")
def test_create_product(mock_create):
    hex = HexBytes("0x000546512314847856")
    mock_create.return_value = hex
    response = client.post(
        "/product/",
        data={
            "name": "test_product",
            "address": "0x0000000000000000000000000000000000000111",
        },
    )

    assert response.status_code == 200
    assert "transaction_hash" in response.get_json()
    assert response.get_json()["transaction_hash"] == hex.hex()

@patch("app.create_product")
def test_create_product_error(mock_create):
    """
    If some error is returned by the create product function, this must be pass forward and return to the api caller.
    """
    mock_create.return_value = {"error": "Some error"}
    response = client.post(
        "/product/",
        data={
            "name": "test_product",
            "address": "0",
        },
    )
    assert response.status_code == 200
    assert response.get_json() == {"transaction_hash": {"error": "Some error"}}

@patch("app.get_product")
def test_read_product(mock_get_prod):
    prod_data = {
        "name": "test_product_0",
        "status": 0,
        "owner": "0x0000000000000000000000000000000000000111",
        "new_owner": "0x0000000000000000000000000000000000000000",
    }
    mock_get_prod.return_value.to_dict.return_value = prod_data
    response = client.get("/product/0")
    assert response.status_code == 200
    assert "product" in response.get_json()
    assert response.get_json()["product"] == prod_data
    mock_get_prod.assert_called_once_with(0)

@patch("app.get_product")
def test_read_product_raise_exception(mock_get_prod):
    mock_get_prod.side_effect = ProductDoesNotExists()
    response = client.get("/product/0")
    assert response.status_code == 200
    assert response.get_json() == {"error": "Product 0 does not exists."}


@patch("app.get_products")
def test_read_products(mock_products):
    prods_data = [
        {
            "name": "test_product_0",
            "status": 0,
            "owner": "0x0000000000000000000000000000000000000111",
            "new_owner": "0x0000000000000000000000000000000000000000",
        },
        {
            "name": "test_product_1",
            "status": 0,
            "owner": "0x0000000000000000000000000000000000000111",
            "new_owner": "0x0000000000000000000000000000000000000000",
        },
    ]
    mock_products.return_value = prods_data
    response = client.get("/")
    assert response.status_code == 200
    assert "products" in response.get_json()
    assert response.get_json()["products"] == prods_data


@patch("app.delegate_product")
def test_delegate_product(mock_delegate):
    hex = HexBytes("0x00982983893492")
    mock_delegate.return_value = hex
    response = client.post(
        "/product/0/delegate/",
        data={
            "address": "0x%040d" % 111,
            "new_address": "0x%040d" % 1,
        },
    )
    assert response.status_code == 200
    # returns a valid transaction hash
    assert response.get_json()["transaction_hash"] == hex.hex()


@patch("app.delegate_product")
def test_delegate_product_error(mock_delegate):
    mock_delegate.return_value = {"error": "Some error"}
    response = client.post(
        "/product/0/delegate/",
        data={
            "address": "0",
            "new_address": "0x%040d" % 111,
        },
    )
    assert response.status_code == 200
    assert response.get_json() == {"transaction_hash": {"error": "Some error"}}


@patch("app.accept_product")
def test_accept_product(mock_accept):
    addr = "0x%040d" % 1
    hex = HexBytes("0x1239234902349012")
    mock_accept.return_value = hex
    response = client.post(
        "/product/0/accept/",
        data={
            "address": addr,
        },
    )
    mock_accept.assert_called_once_with(0, addr)
    assert "transaction_hash" in response.get_json()
    assert response.get_json()["transaction_hash"] == hex.hex()


@patch("app.accept_product")
def test_accept_product_error(mock_accept):
    mock_accept.return_value = {"error": "Some error"}
    response = client.post(
        "/product/0/accept/",
        data={
            "address": "0",
        },
    )
    assert response.status_code == 200
    assert response.get_json() == {"transaction_hash": {"error": "Some error"}}


@patch("app.get_product_by_name")
def test_find_product(mock_find_prod):
    prod_data = {
        "name": "test_product_0",
        "status": 0,
        "owner": "0x%040d" % 111,
        "new_owner": "0x%040d" % 0,
    }
    mock_find_prod.return_value = prod_data
    response = client.get("/product/test_product_0")
    assert response.status_code == 200
    assert response.get_json() == {"product": prod_data}
    mock_find_prod.assert_called_once_with("test_product_0")
