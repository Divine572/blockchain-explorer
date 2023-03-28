from web3 import Web3
from web3.middleware import geth_poa_middleware
import deploy

w3 = Web3(Web3.HTTPProvider('https://alfajores-forno.celo-testnet.org'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)


latest_block_number = w3.eth.block_number
print('Latest block number:', latest_block_number)
block_number = 10
block = w3.eth.get_block(block_number)
print('Block number:', block.number)
print('Block hash:', block.hash.hex())
print('Block timestamp:', block.timestamp)
print('Block transactions:', block.transactions)

if len(block.transactions) > 0:
    tx_hash = block.transactions[0].hex()
    tx = w3.eth.getTransaction(tx_hash)
    print('Transaction hash:', tx.hash.hex())
    print('Transaction sender:', tx['from'])
    print('Transaction receiver:', tx['to'])
    print('Transaction value:', w3.from_wei(tx.value, 'ether'))
else:
    print('No transactions in block', block_number)


contract_address = deploy.contract_address
abi = deploy.abi
contract = w3.eth.contract(address=contract_address, abi=abi)
print('Contract get function:', contract.functions.get().call())
print('Contract set function:', contract.functions.set(2).call())
