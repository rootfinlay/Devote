import datetime #Timestamps
import hashlib #Hash for blocks
import json #Was used for old file strcture but might be used again for flask
import os #General purpose
import threading
import socket

bind_ip = "127.0.0.1"
bind_port = 8199

genesis_block = {
    "block_id" : 0,
    "timestamp" : datetime.datetime.now(),
    "votee" : "GENESIS",
    "vote" : "GENESIS_BLOCK",
    "current_hash" : "d849201979ca8f774b43c29239d41a09fa7de7d65e1c2818cb777c90ffe9aeb3",
    "previous_hash" : "0000000000000000000000000000000000000000000000000000000000000000"
}

def daemon():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_ip, bind_port))
    server.listen(5)

    client, addr = server.accept()
    