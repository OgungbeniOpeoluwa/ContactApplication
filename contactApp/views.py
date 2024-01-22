from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView

from .Services import register_user, add_contact, find_all_contact, find_a_contacts, delete_a_contact, \
    delete_all_contacts, edit_contacts, block_contact, unblock_contact
from .exception import InvalidLoginDetails, UserExistException

import pdb

from .models import Contacts


# Create your views here.
@login_required()
def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['namess']
        last_name = request.POST['surname']
        password = request.POST['password']
        email = request.POST['email']
        phone_number = request.POST['phone']
        address = request.POST['address']
        confirm_password = request.POST['confirmPassword']
        if password == confirm_password:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email is already taken")
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, "username already exist")
                return redirect('register')
            else:
                users = User.objects.create_user(username=username, first_name=name, last_name=last_name, email=email,
                                                 password=password)
                users.save()
                user_model = User.objects.get(username=username)
                user = register_user(user_model, address, phone_number)
                messages.info(request, "you have successfully register")
                return redirect('login')
        else:
            messages.info(request, "Invalid password")
            return redirect('register')
    else:
        return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('views')
        else:
            messages.info(request, "Credentials Invalid")
            return redirect('login')
    else:
        return render(request, 'login.html')


@login_required(login_url='login')
def addContacts(request):
    try:
        if request.method == 'POST':
            user = request.user.username
            users = User.objects.get(username=user)
            user_email = users.email
            name = request.POST['name']
            phone_number = request.POST['phone_number']
            address = request.POST['address']
            email = request.POST['email']
            add_contact(user_email, name, phone_number, address, email)
            return redirect('views')
        else:
            return render(request, 'addContacts.html')
    except UserExistException:
        messages.info(request, "Contact name exist in your contact list")
        return redirect('login')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')


@login_required(login_url='login')
def views(request):
    return render(request, 'views.html')


@login_required(login_url='login')
def search(request):
    user = request.user.username
    users = User.objects.get(username=user)
    email = users.email
    all_user_contact = find_all_contact(email)
    return render(request, 'search.html', {'contacts': all_user_contact})


# class search(ListView):
#     model = Contacts
#     template_name = 'search.html'
def searchbyname(request):
    name = request.POST['name']
    user = request.user.username
    users = User.objects.get(username=user)
    email = users.email
    all_user_contact = find_a_contacts(email, name)
    if all_user_contact is not None:
        return render(request, 'searchbyname.html', {'contact': all_user_contact})

    else:
        messages.info(request, "Name doesn't exist")
        return redirect('views')


def delete(request):
    name = request.GET['name']
    user = request.user.username
    users = User.objects.get(username=user)
    email = users.email
    delete_a_contact(email, name)
    reponse = f'Contact has successfully been deleted'
    return render(request, 'views.html', {'response': reponse})


def deletAll(request):
    user = request.user.username
    users = User.objects.get(username=user)
    email = users.email
    delete_all_contacts(email)
    reponse = f'All Contacts has successfully been deleted'
    return render(request,'views.html',{'response':reponse})


def back(request):
    return render(request, 'views.html')


def editContact(request):
    if request.method == 'POST':
        user = request.user.username
        users = User.objects.get(username=user)
        user_email = users.email
        real_name = request.POST['name']
        name = request.POST['names']
        phone_number = request.POST['phone_number']
        address = request.POST['address']
        email = request.POST['email']
        edit_contacts(user_email, real_name, name, phone_number, address, email)
        return redirect('views')
    else:
        return render(request, 'editContact.html')


def blockContact(request):
    name = request.GET['name']
    user = request.user.username
    users = User.objects.get(username=user)
    email = users.email
    block_contact(email, name)
    response = f'you have successfully block', name, 'from your contact list'
    return render(request, 'views.html',{'response': response})


def unblockContact(request):
    name = request.GET['name']
    user = request.user.username
    users = User.objects.get(username=user)
    email = users.email
    unblock_contact(email, name)
    response = f'you have successfully unblock', name, ' from your contact list'
    return render(request, 'views.html', {'returns': response})
