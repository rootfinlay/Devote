import random
import string
import hashlib
import requests

url = 'http://127.0.0.1:5000/checkvote'

def Main():
    print("========== DEVOTE =========")
    hash_to_get = input("Enter hash to get:\n> ")
    if len(hash_to_get) != 64:
        print("Invalid hash..")
        Main()

    object = {
        'hash' : hash_to_get,
    }

    x = requests.get(url, object)

    print("Response: \n", x.text)



if __name__ == '__main__':
    Main()