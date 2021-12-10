import os
import json
from dotenv import load_dotenv
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware

load_dotenv()

abi = json.loads(open("src/contract_abi.json").read())
w3 = Web3(HTTPProvider(os.getenv("PROVIDER", "https://matic-mumbai.chainstacklabs.com")))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
print(w3.isConnected())

contract_address = "0x94494F7129b2Eb4c3D21bDF80700E963e07179cd"
created_block = 22366976 # contract creation block

contract = w3.eth.contract(address=contract_address, abi=abi)