// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract BlockchainExplorer {

    struct Transaction {
        address sender;
        address recipient;
        uint amount;
        uint timestamp;
    }
    
    struct Contract {
        address contractAddress;
        uint balance;
        uint creationTime;
    }
    
    mapping (address => Transaction[]) private transactions;
    mapping (address => Contract) private contracts;
    
    function getTransactions(address _address) public view returns (Transaction[] memory) {
        return transactions[_address];
    }
    
    function getContract(address _address) public view returns (Contract memory) {
        return contracts[_address];
    }
    
    function searchAddress(address _address) public view returns (Transaction[] memory, Contract memory) {
        return (getTransactions(_address), getContract(_address));
    }
    
    function addTransaction(address _sender, address _recipient, uint _amount) public {
        Transaction memory tx = Transaction(_sender, _recipient, _amount, block.timestamp);
        transactions[_sender].push(tx);
    }
    
    function addContract(address _contractAddress, uint _balance) public {
        Contract memory contractInfo = Contract(_contractAddress, _balance, block.timestamp);
        contracts[_contractAddress] = contractInfo;
    }
    
    function updateContractBalance(address _contractAddress, uint _balance) public {
        contracts[_contractAddress].balance = _balance;
    }
    
}
