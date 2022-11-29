# Devote
Devote - Bringing democracy back to the people

WARNING- This project is NOT ready to be run in production. To learn how to run in a production environment anyway, please see below article
https://www.javacodemonk.com/part-2-deploy-flask-api-in-production-using-wsgi-gunicorn-with-nginx-reverse-proxy-4cbeffdb

WARNING- This is only set to run on localhost, will need extra configuration depending on deployment requirements.

## First things first
```console
# Clone the repo
$ git clone https://github.com/rootfinlay/Devote.git

# Cd into directory
$ cd Devote

# Install requirements
# pip3 install -r requirements.txt
```

## Run the server
```console
$ python blockchain.py
```

## Run the clients
```console
# To run the client
$ python client.py
```

## Run the Devote frontend node
```console
# cd into the directory
$ cd DevoteFrontend

# Run the server
$ python manage.py runserver

# Connect to the website
# 127.0.0.1:8000
```

# Devote in production

Devote in it's current state can be deployed in a production environment, in many different circumstances. 

Contanct me at finlay.business@protonmail.com if you require help with deploying Devote to a production environment and we can discuss the possibilities.

# Public test build
Test Devote (from the public perspective) here: https://rfdevelopments.pythonanywhere.com/ 
There is a default account with the credentials: defaultuser:defaultpassword

/vote - lets you vote
/checkvote - lets you check your vote was counted.