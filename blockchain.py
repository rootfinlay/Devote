#Imports
import datetime #Timestamps
import hashlib
from itertools import chain #Hash for blocks
import json #Was used for old file strcture but might be used again for flask
import os #General purpose
import csv #New file structure
import atexit
from sqlite3 import Timestamp #Handles exit
import random #Used for wallet creation
import string

#Hard coded genesis block - Genesis being first block of chain
genesis_block = {
"block_id" : "0", #Block ID (incremental by one each time) or index
"timestamp" : datetime.datetime.now(), #Current timestamp
"sender" : "GENESIS", #Sender, for genesis block it's just genesis
"block_content" : "GENESIS_BLOCK", #Content for this block, for genesis just "GENESIS_BLOCK"
"current_hash" : "d849201979ca8f774b43c29239d41a09fa7de7d65e1c2818cb777c90ffe9aeb3", #Hash of block content
"previous_hash" : "0000000000000000000000000000000000000000000000000000000000000000", #Previous hash in the chain, because of the genesis block being the first, there won't be a previous hash
"proof_of_work" : "0000000000000000000000000000000000000000000000000000000000000000",
"unique_id_num" : "1"
}

#Add genesis function - writes genesis block to file then adds to chain counter
def addGenesis():
    global chain_counter
    global previous_hash
    #Fiendnames for csv file
    fieldnames = ['block_id', 'timestamp', 'sender', 'block_content', 'current_hash', 'previous_hash', 'proof_of_work', 'unique_id_num']
    #Opens csv file and writes to it.
    with open('main-chain.csv', 'a+', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow(genesis_block)
    f.close()

    chain_counter = chain_counter + 1
    previous_hash = genesis_block.get('current_hash')

    with open('previous_hash.txt', 'w+') as p:
        p.write(previous_hash)

#Creates the actual block then writes to a file and updates chain counter - block needs to be declared in here
def createBlock(blk_content, sender, proof_of_work, unique_id_num):
    global chain_counter
    global previous_hash

    with open('previous_hash.txt', 'r+') as k:
        previous_hash = k.read()

    current_time = datetime.datetime.now()

    with open('chain-length.txt', 'r+') as a:
        chain_counter = int(a.read())

    #Defines block
    block = {
    "block_id" : chain_counter, #Chaincounter variable, updates after every block addition
    "timestamp" : current_time, #Data and time now
    "sender" : sender, #Sender - will have to do front end registration somehow... not sure yet
    "block_content" : recipient, #Content of the block - who is being voted for
    "proof_of_work" : proof_of_work,
    "current_hash" : blkHashScript(sender + recipient + str(current_time) + proof_of_work), #Hashes the block content
    "previous_hash" : previous_hash, # Previous hash from the chain
    "unique_id_num" : unique_id_num
    }

    fieldnames = ['block_id', 'timestamp', 'sender', 'block_content', 'current_hash', 'previous_hash', 'proof_of_work', 'unique_id_num']
    #Appends block to chain
    with open('main-chain.csv', 'a+', newline='') as append_block:
        writer = csv.DictWriter(append_block, fieldnames = fieldnames)

        writer.writerow(block)
    append_block.close()   

    chain_counter = chain_counter + 1
    print("Chaincounter: " + str(chain_counter))

    #Establishes previous hash
    previous_hash = block.get('current_hash')

    with open('previous_hash.txt', 'w+') as o:
        o.write(previous_hash)
        o.close()

    with open('chain-length.txt', 'w+') as p:
        p.write(str(chain_counter))
        p.close()

    return block

#Checks if the genesis block exists
def checkGenesis():
    global chain_counter
    #Opens csv file and sees if string is in it
    with open('main-chain.csv', 'r+') as main_chain_file:
        csv_file = main_chain_file.read()
        if 'GENESIS_BLOCK' in csv_file:
            print('1')
            chain_length_contents = open('chain-length.txt', 'r').read()
            previous_hash = open('previous_hash.txt', 'r').read()
        else:
            chain_counter = 1
            print('2')
            addGenesis()
            open('chain-length.txt', 'w').write("1")
    main_chain_file.close()

#Hashes the transaction data with sha256.. Might implement a different way, might not.
def blkHashScript(blk_content):
    hashed_output = hashlib.sha256(bytes(blk_content, 'utf-8')).hexdigest()
    print(hashed_output)
    return hashed_output

def random_prototype():
    return ''.join([random.choice(string.ascii_letters) for n in range(16)])

def findVote(hash_to_find, id_to_find):
    with open('main-chain.csv', 'r') as chainfile:
        reader = csv.reader(chainfile)
        for row in reader:
            if hash_to_find in row and id_to_find in row:

                return "Vote counted, block: " + str(row)
        return "Vote not counted, or incorrect ID/hash, check spelling and try again"

#Flask initialisation here
from flask import Flask, request, jsonify
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

@app.route('/vote', methods=["POST"])
def vote():
    global sender
    global recipient
    global previous_hash
    if 'recipient' in request.args and 'sender' in request.args and 'proofofwork' in request.args and 'unique_id_num' in request.args:
        recipient = str(request.args['recipient'])
        sender = str(request.args['sender'])
        proof_of_work = str(request.args['proofofwork'])
        unique_id_num = str(request.args['unique_id_num'])
    else:
        return "Invalid args.."

    response = createBlock(recipient, sender, proof_of_work, unique_id_num)

    return jsonify("Block created: \n", response),200

@app.route('/checkvote', methods=["GET"])
def checkvote():
    if 'id' in request.args and 'hash' in request.args:
        hash_to_find = str(request.args['hash'])
        id_to_find = str(request.args['id'])
    else:
        return "Invalid args.."

    response = findVote(hash_to_find, id_to_find)

    return jsonify(response),200

#Check genesis function
if __name__ == '__main__':
    checkGenesis()
    app.run(host='0.0.0.0', port=5000,debug=True)

