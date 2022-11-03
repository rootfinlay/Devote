import random
import string
import hashlib
import requests

url = 'http://127.0.0.1:5000/vote'

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
                print("Proof done")
                proof_of_work = h
                return proof_of_work

def random_prototype():
    return ''.join([random.choice(string.ascii_letters) for n in range(16)])

def Main():
    sender = input("Please enter your name:\n> ")
    recipient = input("Please enter your vote:\n> ")
    proofofwork = proofOfWork()

    object = {
        'sender' : sender,
        'recipient' : recipient,
        'proofofwork' : proofofwork
    }

    x = requests.post(url, params=object)

    print(x.text)



if __name__ == '__main__':
    Main()