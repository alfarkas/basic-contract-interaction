# stdlib
import json
import os

# deps
from dotenv import load_dotenv
from web3 import HTTPProvider, Web3
from web3.middleware import geth_poa_middleware


load_dotenv()

with open("src/contract_abi.json") as contract_file:
    abi = json.loads(contract_file.read())

w3 = Web3(HTTPProvider(os.getenv("PROVIDER", "https://matic-mumbai.chainstacklabs.com")))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
contract_address = w3.toChecksumAddress(
    os.getenv("CONTRACT_ADDR", "0xd9E0b2C0724F3a01AaECe3C44F8023371f845196")
)

created_block = 22660777  # contract creation block

contract = w3.eth.contract(address=contract_address, abi=abi)
