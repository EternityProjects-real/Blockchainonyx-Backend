from web3 import Web3 
import json 

url = "https://mainnet.infura.io/v3/127f027af42b4172a65617a8dfb0121a"

web3 = Web3(Web3.HTTPProvider(url))

print(web3.eth.blockNumber)

print(web3.eth.getBlock(web3.eth.blockNumber))

hash = "0x1ec2e98b58c795cb180fba0ce78cf3d639ee0fe301d09704c5c04fd45e3506d0"

print(web3.eth.getTransactionByBlock(hash, 2))