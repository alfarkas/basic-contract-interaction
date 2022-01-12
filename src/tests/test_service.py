# stdlib
import json
import os
from unittest.mock import patch

# deps
from dotenv import load_dotenv
from eth_account.datastructures import SignedTransaction
from hexbytes import HexBytes

# local
from service import app


load_dotenv()

client = app.test_client()


@patch("service.w3.eth.account.sign_transaction")
def test_api_sign_tx(mock_sign, monkeypatch):
    monkeypatch.setenv("KEY", "fake-key", prepend=False)
    mock_sign.return_value = SignedTransaction(
        rawTransaction=HexBytes(
            "0xf8cc808504a817c8008303345094600757547255aa29430612d3155dde9a0bb"
        ),
        hash=HexBytes("0xf541db9896ba7b557b8635b4880556ddfe"),
        r=5807941984468536703127644958600620555,
        s=3850855411775802047747259,
        v=2710,
    )
    json_data = (
        json.dumps(
            {
                "value": 0,
                "chainId": 1337,
                "from": "0x%040d" % 321,
                "gas": 210000,
                "gasPrice": 20000000000,
                "nonce": 1,
                "to": "0x%040d" % 123,
                "data": "0x02ec06be00000000000",
            }
        ),
    )

    response = client.get("/", json=json_data[0])
    mock_sign.assert_called_once_with(json.loads(json_data[0]), os.environ["KEY"])
    assert response.status_code == 200
    json_response = response.get_json()
    assert "rawTransaction" in json_response
    assert "hash" in json_response
    assert "r" in json_response
    assert "s" in json_response
    assert "v" in json_response
    assert json_response["rawTransaction"] == HexBytes(
            "0xf8cc808504a817c8008303345094600757547255aa29430612d3155dde9a0bb"
        ).hex()
    assert json_response["hash"] == HexBytes("0xf541db9896ba7b557b8635b4880556ddfe").hex()
    assert json_response["r"] == 5807941984468536703127644958600620555
    assert json_response["s"] == 3850855411775802047747259
    assert json_response["v"] == 2710


def test_api_sign_tx_no_tx():
    response = client.get("/", json=json.dumps({}))
    assert "error" in response.get_json()
    assert response.get_json()["error"] == "A transaction must be provided"


@patch("service.w3.eth.account.sign_transaction")
def test_api_sign_tx_error(mock_sign, monkeypatch):
    monkeypatch.setenv("KEY", "fake-key", prepend=False)
    json_data = (
        json.dumps(
            {
                "value": 0,
                "chainId": 1337,
                "from": "0x%040d" % 321,
                "gas": 210000,
                "gasPrice": 20000000000,
                "nonce": 1,
                "to": "0x%040d" % 123,
                "data": "0x02ec06be00000000000",
            }
        ),
    )
    mock_sign.side_effect = Exception("fake error")
    response = client.get("/", json=json_data[0])
    assert "error" in response.get_json()
    assert response.get_json()["error"] == "fake error"