import random
import string
import hashlib
import requests

def proofOfWork(level=5):
    proof_count = 0
    prototype = random_prototype()
    h = ''
    while True:
        for pow in range(0, 512):
            temp_string = ''.join(prototype)
            temp_string = temp_string.join(str(pow+random.randint(1,4096)*random.randint(1,4096)))
            h = hashlib.sha256(bytes(temp_string, encoding='utf-8')).hexdigest()
            proof_count += 1
            if h[0:level] == ('0' * level):
                proof_of_work = h
                print("\nProof done: ", proof_of_work, "\n")
                return proof_of_work

def random_prototype():
    return ''.join([random.choice(string.ascii_letters) for n in range(16)])

def Vote():
    url = 'http://127.0.0.1:5000/vote'
    sender = input("Please enter your name:\n> ")
    recipient = input("Please enter your vote:\n> ")
    unique_id = input("Please enter your voter ID:\n> ")
    proofofwork = proofOfWork()

    object = {
        'sender' : sender,
        'recipient' : recipient,
        'proofofwork' : proofofwork,
        'unique_id_num' : unique_id
    }

    x = requests.post(url, params=object)

    print("Response:\n", x.text)

def CheckVote():
    url = 'http://127.0.0.1:5000/checkvote'
    id_to_get = input("Enter ID of voter to get:\n> ")
    hash_to_get = input("Enter hash to get:\n> ")
    if len(hash_to_get) != 64:
        print("Invalid hash..")
        Main()

    if len(id_to_get) > 15:
        print("Invalid ID")
        Main()

    object = {
        'id' : id_to_get,
        'hash' : hash_to_get,
    }

    x = requests.get(url, object)

    print("Response: \n", x.text)

def Main():
    print("========== DEVOTE ==========")
    choice = input("Press 1 to vote and 2 to check if your vote was registered.\n>  ")
    if choice == "1":
        Vote()
    elif choice == "2":
        CheckVote()
    else:
        print("Invalid option")
        Main()

if __name__ == '__main__':
    Main()