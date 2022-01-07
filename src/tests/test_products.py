# deps
import pytest

# local
from src.exceptions import ProductDoesNotExists
from src.products import (
    accept_product,
    contract,
    create_product,
    delegate_product,
    get_product,
    get_product_by_name,
    get_products,
)
from src.tests.fixtures import *


def test_create_product(product_contract, mock_contract, mock_w3, account_1):
    create_product("prod_1", account_1.address, account_1.key)
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


def test_account_cannot_create_more_than_eleven_products(mock_contract, mock_w3, account_1):
    for i in range(12):
        create_product("test_product", account_1.address, account_1.key)

    products = get_products()
    assert len(products) == 11


def test_delegate_product(
    product_contract, mock_contract, mock_w3, account_1, account_2, new_product
):
    # get the created product
    created_product = get_product(0)
    assert created_product[1] == 0
    assert created_product[2] == account_1.address
    assert created_product[3] == "0x0000000000000000000000000000000000000000"

    delegate_product(0, account_1.address, account_1.key, account_2.address)

    # get the delegated product
    delegated_product = get_product(0)
    assert delegated_product[1] == 1
    assert delegated_product[2] == account_1.address
    assert delegated_product[3] == account_2.address


def test_accept_product(mock_contract, mock_w3, account_1, account_2, new_product):
    delegate_product(0, account_1.address, account_1.key, account_2.address)
    # get the delegated product
    delegated_product = get_product(0)
    assert delegated_product[1] == 1
    assert delegated_product[2] == account_1.address
    assert delegated_product[3] == account_2.address

    accept_product(0, account_2.address, account_2.key)

    # get the accepted product
    accepted_product = get_product(0)

    assert accepted_product[1] == 0
    assert accepted_product[2] == account_2.address
    assert accepted_product[3] == "0x0000000000000000000000000000000000000000"


@pytest.mark.parametrize("new_product", [10], indirect=True)
def test_get_all_products(mock_contract, mock_w3, account_1, new_product):
    products = get_products()
    for i in range(0, len(products)):
        assert products[i][0] == "new_prod_" + str(i)
        assert products[i][1] == 0
        assert products[i][2] == account_1.address
        assert products[i][3] == "0x0000000000000000000000000000000000000000"

    assert len(products) == 10


@pytest.mark.parametrize("mock_products", [10], indirect=True)
def test_get_product_by_name(mock_products):
    products = get_product_by_name("prod_name_5")
    assert len(products) == 1
    assert products[0][0] == "prod_name_5"
    assert products[0][1] == 0
    assert products[0][2] == "0x1234567890"
    assert products[0][3] == "0x0987654321"
