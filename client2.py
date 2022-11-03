import random
import string
import hashlib
import requests

url = 'http://127.0.0.1:5000/checkvote'

def Main():
    hash_to_get = input("Enter hash to get:\n> ")

    object = {
        'hash' : hash_to_get,
    }

    x = requests.get(url, object)

    print(x.text)



if __name__ == '__main__':
    Main()