# stdlib
import json
import os

# flask
from flask import Flask, jsonify, request

# local
from src.connection import w3


app = Flask(__name__)


@app.route("/")
def sign():
    tx = json.loads(request.get_json())
    if not tx:
        return jsonify({"error": "A transaction must be provided"})
    key = os.environ["KEY"]
    try:
        signed_tx = w3.eth.account.sign_transaction(tx, key)
    except Exception as e:
        return jsonify({"error": str(e.args[0])})
    return jsonify(
        {
            "rawTransaction": signed_tx["rawTransaction"].hex(),
            "hash": signed_tx["hash"].hex(),
            "r": signed_tx["r"],
            "s": signed_tx["s"],
            "v": signed_tx["v"],
        }
    )
