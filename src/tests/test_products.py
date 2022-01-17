# stdlib
from unittest.mock import MagicMock, patch

# deps
import pytest

# local
from src.exceptions import ProductDoesNotExists
from src.products import (
    accept_product,
    create_product,
    delegate_product,
    get_delegated_products,
    get_delegated_products_by_owner,
    get_product,
    get_product_by_name,
    get_products,
    send_transaction,
)
from src.tests.fixtures import *


def test_send_transaction_invalid_addr(mock_w3):
    mock_build_tx = MagicMock()
    ret = send_transaction(mock_build_tx, "fake-address")
    assert ret == {"error": "Invalid address"}


@patch("src.products.w3.eth.get_transaction_count")
@patch("src.products.print")
@patch("src.products.requests.request")
def test_send_transaction_request_error(mock_request, mock_print, mock_get_txc, mock_w3):
    mock_build_tx = MagicMock()
    mock_build_tx.buildTransaction.return_value = {"rawTransaction": "fake tx"}
    mock_request.side_effect = Exception("Some exception")
    ret = send_transaction(mock_build_tx, "fake-address")
    assert ret == {"error": "Something went wrong, try again."}
    mock_print.assert_called_once_with("Some exception")


def test_create_product(mock_request, product_contract, mock_contract, mock_w3, account_1):
    create_product("prod_1", account_1.address)
    # get the created product
    created_product = product_contract.functions.products(0).call()

    assert created_product[0] == "prod_1"
    assert created_product[1] == 0
    assert created_product[2] == account_1.address
    assert created_product[3] == "0x0000000000000000000000000000000000000000"


def test_get_product(product_contract, mock_contract, mock_w3, account_1, new_product):
    product = product_contract.functions.products(0).call()

    assert product[0] == "new_prod"
    assert product[1] == 0
    assert product[2] == account_1.address
    assert product[3] == "0x0000000000000000000000000000000000000000"


def test_get_product_raise_exception(mock_exception):
    with pytest.raises(ProductDoesNotExists):
        get_product(0)


def test_account_cannot_create_more_than_eleven_products(
    mock_request, mock_contract, mock_w3, account_1
):
    for i in range(12):
        create_product("test_product", account_1.address)

    products = get_products()
    assert len(products) == 11


def test_delegate_product(
    mock_request, product_contract, mock_contract, mock_w3, account_1, account_2, new_product
):
    # get the created product
    created_product = get_product(0)
    assert created_product.status == 0
    assert created_product.owner == account_1.address
    assert created_product.new_owner == "0x0000000000000000000000000000000000000000"

    delegate_product(0, account_1.address, account_2.address)

    # get the delegated product
    delegated_product = get_product(0)
    assert delegated_product.status == 1
    assert delegated_product.owner == account_1.address
    assert delegated_product.new_owner == account_2.address


@patch("src.products.send_transaction")
@patch("src.products.contract.functions.acceptProduct")
def test_accept_product(mock_accept, mock_send_tx):
    tx = "fake-tx"
    addr = "0x%040d" % 1
    mock_accept.return_value = tx
    accept_product(0, addr)
    mock_accept.assert_called_once_with(0)
    mock_send_tx.assert_called_once_with(tx, addr)


@pytest.mark.parametrize("new_product", [10], indirect=True)
def test_get_all_products(mock_contract, mock_w3, account_1, new_product):
    products = get_products()
    for i in range(0, len(products)):
        assert products[i]["name"] == "new_prod_" + str(i)
        assert products[i]["status"] == 0
        assert products[i]["owner"] == account_1.address
        assert products[i]["new_owner"] == "0x0000000000000000000000000000000000000000"

    assert len(products) == 10


@pytest.mark.parametrize("mock_products", [10], indirect=True)
def test_get_product_by_name(mock_products):
    products = get_product_by_name("prod_name_5")
    assert len(products) == 1
    assert products[0]["name"] == "prod_name_5"
    assert products[0]["status"] == 0
    assert products[0]["owner"] == "0x%040d" % 0
    assert products[0]["new_owner"] == "0x%040d" % 0


@patch("src.products.print")
@patch("src.products.contract.functions.size")
@patch("src.products.get_product")
def test_get_products_exception(mock_get_product, mock_size, mock_print):
    mock_get_product.return_value.to_dict.side_effect = [
        {"name": "fake-prod-1", "status": 0, "owner": "0x%040d" % 0, "new_owner": "0x%040d" % 0},
        ProductDoesNotExists,
    ]
    msize = MagicMock()
    msize.call.return_value = 2
    mock_size.return_value = msize
    products = get_products()
    mock_print.assert_called_once_with("Unable to get product 1")
    assert len(products) == 1


@pytest.mark.parametrize("mock_products", [10], indirect=True)
def test_get_delegated_products(mock_products):
    delegate_products = get_delegated_products()
    assert len(delegate_products) == 5
    for dp in delegate_products:
        assert dp["status"] == 1


@patch("src.products.get_products")
def test_get_delegated_products_by_owner(mock_products):
    mock_products.return_value = [
        {"owner": "0x%040d" % 1},
        {"owner": "0x%040d" % 1},
        {"owner": "0x%040d" % 1},
        {"owner": "0x%040d" % 1},
        {"owner": "0x%040d" % 0},
        {"owner": "0x%040d" % 0},
    ]
    owner_products = get_delegated_products_by_owner("0x%040d" % 1)
    assert len(owner_products) == 4
    for op in owner_products:
        assert op["owner"] == "0x%040d" % 1
