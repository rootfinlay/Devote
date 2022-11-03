import random
import string
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def WalletCreate():
    priv_key = rsa.generate_private_key(public_exponent=65537, key_size=4096)
    print(priv_key)
    

if __name__ == '__main__':
    WalletCreate()