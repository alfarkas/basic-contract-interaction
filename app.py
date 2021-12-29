# stdlib
import json

# flask
from flask import Flask, request

# local
from src.exceptions import ProductDoesNotExists
from src.products import (
    Web3,
    accept_product,
    delegate_product,
    get_product,
    get_product_by_name,
    get_products,
)


app = Flask(__name__)


@app.route("/")
def products():
    products = get_products()
    return Web3.toJSON(products)


@app.route("/product/<int:prod_id>")
def product(prod_id):
    try:
        product = get_product(prod_id)
    except ProductDoesNotExists:
        return json.dumps({"error": f"Product {prod_id} does not exists."})
    return Web3.toJSON(product)


@app.route("/product/<prod_name>")
def find_product(prod_name):
    product = get_product_by_name(prod_name)
    return Web3.toJSON(product)


@app.route("/product/", methods=["POST"])
def create_product():
    product = create_product(request.form["address"], request.form["key"])
    return Web3.toJSON(product)


@app.route("/product/<int:prod_id>/delegate/", methods=["POST"])
def delegate_product(prod_id):
    product = delegate_product(prod_id, request.form["address"], request.form["key"])
    return Web3.toJSON(product)


@app.route("/product/<int:prod_id>/accept/", methods=["POST"])
def accept_product(prod_id):
    product = accept_product(prod_id, request.form["address"], request.form["key"])
    return Web3.toJSON(product)
