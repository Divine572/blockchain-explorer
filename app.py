from web3 import Web3
from web3.middleware import geth_poa_middleware
import deploy

w3 = deploy.w3
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

contract_address = deploy.contract_address
abi = deploy.abi

# Instantiate the contract object
contract = w3.eth.contract(address=contract_address, abi=abi)

# Check account balance
balance = w3.eth.get_balance('0x8BdDeC1b7841bF9eb680bE911bd22051f6a00815')
print(f'Account balance: {balance}')


# # Add a new transaction
# tx_hash = contract.functions.addTransaction(
#     contract_address, '0xcdd1151b2bC256103FA2565475e686346CeFd813', 100).transact()

# # Wait for the transaction to be mined
# w3.eth.wait_for_transaction_receipt(tx_hash)

# # Add a new contract
# tx_hash = contract.functions.addContract(
#     '0x0987654321098765432109876543210987654321', 1000).transact()

# # Wait for the transaction to be mined
# w3.eth.wait_for_transaction_receipt(tx_hash)


# # Update contract balance
# tx_hash = contract.functions.updateContractBalance(
#     '0x8BdDeC1b7841bF9eb680bE911bd22051f6a00815', 2000).transact()

# # Wait for the transaction to be mined
# w3.eth.wait_for_transaction_receipt(tx_hash)


# Call the getTransactions function
transactions = contract.functions.getTransactions(
    '0x8BdDeC1b7841bF9eb680bE911bd22051f6a00815').call()

# Print the transaction data
for tx in transactions:
    print(
        f'Sender: {tx[0]}, Recipient: {tx[1]}, Amount: {tx[2]}, Timestamp: {tx[3]}')


# Call the getContract function
contract_info = contract.functions.getContract(
    '0x8BdDeC1b7841bF9eb680bE911bd22051f6a00815').call()

# Print the contract information
print(
    f'Address: {contract_info[0]}, Balance: {contract_info[1]}, Creation Time: {contract_info[2]}')


# Call the searchAddress function
transactions, contract_info = contract.functions.searchAddress(
    '0x8BdDeC1b7841bF9eb680bE911bd22051f6a00815').call()


# Print the transaction data
for tx in transactions:
    print(
        f'Sender: {tx[0]}, Recipient: {tx[1]}, Amount: {tx[2]}, Timestamp: {tx[3]}')
