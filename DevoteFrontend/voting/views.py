from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
import requests, random, hashlib, string
import hashlib

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('/vote')
    elif not request.user.is_authenticated:
        target_page = "index.html"

    return render(request, target_page)

@login_required(login_url = '/login')
def vote(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    
    if request.method=="POST":
        url = 'http://127.0.0.1:5000/vote'
        recipient = request.POST['vote']
        sender = request.POST['sender']
        unique_id_num = request.POST['uniqueidcode']
        proofofwork = proofOfWork(5)

        object = {
        'sender' : sender,
        'recipient' : recipient,
        'proofofwork' : proofofwork,
        'unique_id_num' : unique_id_num
    }

        x = requests.post(url, params=object)

        voter = Voters(name=sender, username=request.user , identifier=unique_id_num, block=x.text)
        voter.save()

        context = {
            "returned_block" : x.text
        }
        return render(request, "voted.html", context)


    return render(request, "vote.html")

#Proof of work done client side
def proofOfWork(level):
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

def UserRegister(request):
    if request.user.is_authenticated:
        return redirect('/vote')
    if request.method=="POST":   
        username = request.POST['username']
        email = request.POST['email']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        password = hashlib.sha256(request.POST['password'].encode('utf-8')).hexdigest()
        confirm_password = hashlib.sha256(request.POST['confirm_password'].encode('utf-8')).hexdigest()

        if len(username) > 15:
            messages.error(request, "Username must be under 15 characters.")
            return redirect('/register')
        if not username.isalnum():
            messages.error(request, "Username must contain only letters and numbers.")
            return redirect('/register')
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('/register')
        
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return redirect('/login')        
    return render(request, "register.html")

def UserLogin(request):
    if request.method=="POST":
        username = request.POST['username']
        password = hashlib.sha256(request.POST['password'].encode('utf-8')).hexdigest()
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/vote")
        else:
            messages.error(request, "Invalid Credentials")
        return render(request, 'login.html')            
    return render(request, "login.html")

@login_required(login_url = '/login')
def UserLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/login')

@login_required(login_url = '/login')
def CheckVote(request):
    url = 'http://127.0.0.1:5000/checkvote'
    if request.method=="POST":
        id_to_get = request.POST['uniqueidcode']
        hash_to_get = request.POST['hash']

        if len(hash_to_get) != 64:
            messages.error(request, "Invalid hash")
            return redirect("/checkvote")
        
        object = {
        'id' : id_to_get,
        'hash' : hash_to_get,
        }

        x = requests.get(url, object)
        context = {
            "returned_info" : x.text
        }

        return render(request, "votechecked.html", context)
    return render(request, "checkvote.html")