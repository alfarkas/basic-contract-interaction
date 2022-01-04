# stdlib
import json

# flask
from flask import Flask, request

# deps
from web3 import Web3

# local
from src.exceptions import ProductDoesNotExists
from src.products import (
    accept_product,
    create_product,
    delegate_product,
    get_product,
    get_product_by_name,
    get_products,
)


app = Flask(__name__)


@app.route("/")
def products():
    products = get_products()
    return {"products": products}


@app.route("/product/<int:prod_id>")
def product(prod_id):
    try:
        product = get_product(prod_id)
    except ProductDoesNotExists:
        return {"error": f"Product {prod_id} does not exists."}
    return {"product": json.loads(Web3.toJSON(product))}


@app.route("/product/<prod_name>")
def find(prod_name):
    product = get_product_by_name(prod_name)
    return {"product": json.loads(Web3.toJSON(product))}


@app.route("/product/", methods=["POST"])
def add():
    product = create_product(request.form["name"], request.form["address"], request.form["key"])
    return {"transaction_hash": json.loads(Web3.toJSON(product))}


@app.route("/product/<int:prod_id>/delegate/", methods=["POST"])
def delegate(prod_id):
    product = delegate_product(prod_id, request.form["address"], request.form["key"], request.form["new_address"])
    return {"transaction_hash": json.loads(Web3.toJSON(product))}


@app.route("/product/<int:prod_id>/accept/", methods=["POST"])
def accept(prod_id):
    product = accept_product(prod_id, request.form["address"], request.form["key"])
    return {"transaction_hash": json.loads(Web3.toJSON(product))}
