#Imports
import datetime #Timestamps
import hashlib #Hash for blocks
import json #Was used for old file strcture but might be used again for flask
import os #General purpose
import csv #New file structure
import atexit #Handles exit

#Hard coded genesis block - Genesis being first block of chain
genesis_block = {
"block_id" : "0", #Block ID (incremental by one each time) or index
"timestamp" : datetime.datetime.now(), #Current timestamp
"sender" : "GENESIS", #Sender, for genesis block it's just genesis
"block_content" : "GENESIS_BLOCK", #Content for this block, for genesis just "GENESIS_BLOCK"
"current_hash" : "d849201979ca8f774b43c29239d41a09fa7de7d65e1c2818cb777c90ffe9aeb3", #Hash of block content
"previous_hash" : "0000000000000000000000000000000000000000000000000000000000000000" #Previous hash in the chain, because of the genesis block being the first, there won't be a previous hash
}

#Add genesis function - writes genesis block to file then adds to chain counter
def addGenesis():
    global chain_counter
    #Fiendnames for csv file
    fieldnames = ['block_id', 'timestamp', 'sender', 'block_content', 'current_hash', 'previous_hash']
    #Opens csv file and writes to it.
    with open('main-chain.csv', 'a+', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow(genesis_block)

    chain_counter = chain_counter + 1
    previous_hash = genesis_block.get('previous_hash')
    print(previous_hash)

#Creates the actual block then writes to a file and updates chain counter - block needs to be declared in here
def createBlock():
    global chain_counter
    #Defines block
    block = {
    "block_id" : chain_counter, #Chaincounter variable, updates after every block addition
    "timestamp" : datetime.datetime.now(), #Data and time now
    "sender" : sender, #Sender - will have to do front end registration somehow... not sure yet
    "block_content" : blk_content, #Content of the block - who is being voted for
    "current_hash" : blkHashScript(blk_content), #Hashes the block content
    "previous_hash" : previous_hash # Previous hash from the chain
    }

    fieldnames = ['block_id', 'timestamp', 'sender', 'block_content', 'current_hash', 'previous_hash']
    #Appends block to chain
    with open('main-chain.csv', 'a+', newline='') as append_block:
        writer = csv.DictWriter(append_block, fieldnames = fieldnames)

        writer.writeheader()
        writer.writerow(block)

    #Adds to chain counter
    chain_counter = chain_counter + 1
    previous_hash = block.get('previous_hash')

#Checks if the genesis block exists
def checkGenesis():
    global chain_counter
    #Opens csv file and sees if string is in it
    with open('main-chain.csv', 'r+') as main_chain_file:
        csv_file = main_chain_file.read()
        if 'GENESIS_BLOCK' in csv_file:
            print('1')
            chain_length_contents = open('chain-length.txt', 'r').read()
            chain_counter = int(chain_length_contents)
        else:
            chain_counter = 0
            print('2')
            addGenesis()

#Hashes the transaction data with sha256.. Might implement a different way, might not.
def blkHashScript(blk_content):
    hashed_output = hashlib.sha256(bytes(blk_content, 'utf-8')).hexdigest()
    print(hashed_output)
    return hashed_output

#Exit handler handles the exiting of a program
def exit_handler():
    global chain_counter
    chain_length = str(chain_counter)
    with open('chain-length.txt', 'w') as x:
        x.write(chain_length)

if __name__ == '__main__':
    checkGenesis()

#Register the function that runs at the end
atexit.register(exit_handler)
