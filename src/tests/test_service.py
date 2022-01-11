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
            "0xf8cc808504a817c80083033450946fd6c4126515869850ea5fdb753af31c49b3633b80b86402ec06be000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000096161616161626262620000000000000000000000000000000000000000000000820a96a08067c96529a2cdb4711b731e882f013f5dde7233cc92b6f9ca5f42be1abe6a0ba0088381c5c9a4936765380486a67ce986757547255aa29430612d3155dde9a0bb"
        ),
        hash=HexBytes("0xf541db9896ba7b557b863b0ca0d9d15d6bd40648657c212c8835b4880556ddfe"),
        r=58079419844685367031201585851489716358059542391153495572958807644958600620555,
        s=3850855411775802046712650899237207108130074652383547787984807264744047747259,
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
    # assert response.get_json() == {
    #    "rawTransaction": ["rawTransaction"],
    #    "hash": "hash",
    #    "r": "r",
    #    "s": "s",
    #    "v": "v",
    # }
