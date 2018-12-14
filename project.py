import json
import hashlib
import sys
from web3 import Web3, HTTPProvider, IPCProvider
from pprint import pprint
from random import randrange
web3 = Web3 (HTTPProvider ("http://localhost:9545"))

###### READ THE FILE ########

with open ("projectabi.json") as f:
    abi = json.load (f)

###### CONTRACT ADDRESS #####
if len (sys.argv) == 2:
    contract_address = sys.argv[1]
else:
    block_number = web3.eth.blockNumber
    contract_address = None
    while contract_address == None and block_number >= 0:
        block = web3.eth.getBlock (block_number)
        for tx_hash in block.transactions:
            tx = web3.eth.getTransactionReceipt (tx_hash)
            contract_address = tx.get ("contractAddress") 
            if contract_address != None:
                break
        block_number = block_number - 1
contract = web3.eth.contract (abi = abi, address = contract_address)
print ("Using contract address {:s}\n".format (contract_address))
print()
print("Pick a number between 1-200")
print()

######### PLAY  ##########
def play(account_index,n,r):
    account = web3.eth.accounts[account_index]
    print ("Using account {:d} with address {:s} to play on contract {:s}".format (account_index, account, contract_address))
    data = int.to_bytes (n, 32, "big") + int.to_bytes (r, 32, "big")
    hash_nr = hashlib.sha256 (data).hexdigest ()
    transaction_hash = contract.transact ({
        "from": account,
        "value": web3.toWei (2, "ether")
    }).play (Web3.toBytes (hexstr = hash_nr));

play(1,100,394356)
play(2,50,231902)
play(3,100,832970)
play(4,100,576848)
play(5,20,343203)

##### BALANCES ####
def printBalances ():
    for acc in web3.eth.accounts:
        balance = web3.eth.getBalance (acc)
        print ("{:s} has {:.020f} ETH".format (acc, float (web3.fromWei (balance, "ether"))))
    print ()

print ()
printBalances ()

######### WINNING ##########
account = web3.eth.accounts[0]
transaction_hash = contract.transact ({
    "from": account
}).winning (100);
print("Winning number is : 100")
print()

######### REVEAL ##########
def reveal(account_index,r):
    account = web3.eth.accounts[account_index]
    print ("Using account {:d} with address {:s} to reveal on contract {:s}".format (account_index, account, contract_address))
    transaction_hash = contract.transact ({
        "from": account
    }).reveal (r);

reveal(1,394356)
reveal(3,832970)
reveal(4,576848)


##### DONE ####### 
account = web3.eth.accounts[0]
transaction_hash = contract.transact ({
"from": account}).done ();


print("Final Balances Are:")
print ()
printBalances ()
