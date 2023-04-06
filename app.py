import os
from web3 import Web3
from web3.middleware import geth_poa_middleware
from dotenv import load_dotenv

load_dotenv()

# Set up web3 connection
provider_url = os.environ.get("CELO_PROVIDER_URL")
w3 = Web3(Web3.HTTPProvider(provider_url))
assert w3.is_connected(), "Not connected to a Celo node"

w3.middleware_onion.inject(geth_poa_middleware, layer=0)


# Retrieving Transaction and Block Data
latest_block_number = w3.eth.block_number
print(f'Latest Block Number: {latest_block_number}')


# To get the details of a specific block:
block_number = 1000
block = w3.eth.get_block(block_number)
print(f'Block {block_number} details: {block}')

# To obtain transaction details by transaction hash:
transaction_hash = '0x8c183dc066cc5ece0e4f6cf9a0dcfb4965c6af496d2985df8356d24275717759'
transaction = w3.eth.get_transaction(transaction_hash)
print(f'Transaction details: {transaction}')


# To check the balance of a specific wallet address:
address = '0x8BdDeC1b7841bF9eb680bE911bd22051f6a00815'
balance = w3.eth.get_balance(address)
print(f'Address balance: {balance} Celo')


def main():
    print('Welcome to the Celo Blockchain Explorer!')
    while True:
        user_input = input('Enter a command (h for help): ').lower()
        if user_input == 'h':
            print_help()
        elif user_input == 'q':
            break
        else:
            handle_command(user_input)


def print_help():
    print('Commands:')
    print('  h - Display help')
    print('  q - Quit the explorer')
    print('  block <block_number> - Show block details')
    print('  tx <transaction_hash> - Show transaction details')
    print('  balance <wallet_address> - Show wallet balance')


def handle_command(command):
    cmd_parts = command.split()
    if len(cmd_parts) == 0:
        return
    cmd = cmd_parts[0]
    if cmd == 'block':
        show_block_details(cmd_parts[1:])
    elif cmd == 'tx':
        show_transaction_details(cmd_parts[1:])
    elif cmd == 'balance':
        show_wallet_balance(cmd_parts[1:])
    elif cmd == 'search':
        search_data(cmd_parts[1:])
    elif cmd == 'stats':
        show_network_stats()
    elif cmd == 'contract':
        show_contract_details(cmd_parts[1:])
    else:
        print('Invalid command. Type "h" for help.')


def search_data(args):
    if len(args) != 1:
        print('Invalid search query. Please provide a valid transaction hash, block hash, or wallet address.')
        return

    query = args[0]
    if query.startswith('0x'):
        if len(query) == 66:
            show_transaction_details([query])
        elif len(query) == 42:
            show_wallet_balance([query])
        else:
            show_block_details([query])
    else:
        show_block_details([query])


def show_network_stats():
    latest_block = w3.eth.get_block('latest')
    block_number = latest_block['number']
    gas_used = latest_block['gasUsed']
    avg_block_time = (
        latest_block['timestamp'] - w3.eth.get_block(block_number - 100)['timestamp']) / 100

    print(f'Total blocks: {block_number}')
    print(f'Latest block gas used: {gas_used}')
    print(
        f'Average block time (last 100 blocks): {avg_block_time:.2f} seconds')


def show_transaction_details(args):
    if len(args) != 1:
        print('Invalid transaction hash. Please provide a valid transaction hash.')
        return

    transaction_hash = args[0]
    transaction = w3.eth.get_transaction(transaction_hash)
    if transaction is None:
        print('Transaction not found.')
        return
    
    ERC20_ABI = [
        {
            "constant": true,
            "inputs": [],
            "name": "totalSupply",
            "outputs": [{"name": "", "type": "uint256"}],
            "payable": false,
            "stateMutability": "view",
            "type": "function"
        },
        {
            "constant": true,
            "inputs": [{"name": "owner", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"name": "", "type": "uint256"}],
            "payable": false,
            "stateMutability": "view",
            "type": "function"
        },
        {
            "constant": false,
            "inputs": [
                {"name": "to", "type": "address"},
                {"name": "value", "type": "uint256"}
            ],
            "name": "transfer",
            "outputs": [{"name": "", "type": "bool"}],
            "payable": false,
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "constant": true,
            "inputs": [
                {"name": "owner", "type": "address"},
                {"name": "spender", "type": "address"}
            ],
            "name": "allowance",
            "outputs": [{"name": "", "type": "uint256"}],
            "payable": false,
            "stateMutability": "view",
            "type": "function"
        },
        {
            "constant": false,
            "inputs": [
                {"name": "spender", "type": "address"},
                {"name": "value", "type": "uint256"}
            ],
            "name": "approve",
            "outputs": [{"name": "", "type": "bool"}],
            "payable": false,
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "constant": false,
            "inputs": [
                {"name": "from", "type": "address"},
                {"name": "to", "type": "address"},
                {"name": "value", "type": "uint256"}
            ],
            "name": "transferFrom",
            "outputs": [{"name": "", "type": "bool"}],
            "payable": false,
            "stateMutability": "nonpayable",
            "type": "function"
        }
    ]


    # Check if the transaction involves a token transfer
    if transaction['input'].startswith('0xa9059cbb'):
        token_contract = w3.eth.contract(
            address=transaction['to'], abi=ERC20_ABI)
        recipient = '0x' + transaction['input'][34:74]

        token_amount = int(transaction['input'][74:], 16) / \
            (10 ** token_contract.functions.decimals().call())


        token_symbol = token_contract.functions.symbol().call()
        print(f'Token transfer: {token_amount} {token_symbol} -> {recipient}')
    else:
        print(f'Transaction details: {transaction}')




if __name__ == '__main__':
    main()
