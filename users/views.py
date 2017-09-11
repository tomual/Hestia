import random
import requests
import json
import urllib.request
import os.path

from pathlib import Path
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission, User
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from users.models import Profile
from .forms import UserForm, LoginForm, RegisterForm

def index(request):
    users_all = User.objects.all()

    paginator = Paginator(users_all, 10)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        users = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        users = paginator.page(paginator.num_pages)
    page_numbers = range(1, paginator.num_pages + 1)

    return render(request, 'users/index.html', {'users':users, 'page_numbers':page_numbers})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Invalid login')
        return render(request, 'users/login.html', {'form':form})
    else:
        form = LoginForm()
        return render(request, 'users/login.html', {'form':form})

def logout_view(request):
    logout(request)
    return redirect('/')

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.create_user(username, email, password)
            except IntegrityError as e:
                messages.error(request, 'Username taken')
                return render(request, 'users/register.html', {'form':form})
            profile = Profile.objects.create(user=user)
            login(request, user)
            return redirect('/')
        return render(request, 'users/register.html', {'form':form})
    else:
        form = RegisterForm()
        return render(request, 'users/register.html', {'form':form})

def profile(request, username):
    profile_user = User.objects.get(username=username)
    return render(request, 'users/profile.html', {'profile_user':profile_user})

def edit(request):
    user_edit = User.objects.get(username=request.user.username)
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES)

        if form.is_valid():
            user_edit.email = form.cleaned_data['email']
            user_edit.profile.location = form.cleaned_data['location']
            user_edit.profile.description = form.cleaned_data['description']
            if request.FILES.get('icon', False):
                user_edit.profile.icon = form.cleaned_data['icon']
            user_edit.profile.save()
            user_edit.save()

        return render(request, 'users/edit.html', {'form':form})
    else:
        data = {
            'username': user_edit.username,
            'email': user_edit.email,
            'location': user_edit.profile.location,
            'description': user_edit.profile.description,
        }
        form = UserForm(initial=data)
        return render(request, 'users/edit.html', {'form':form})

def generate_users(request):
    number = 10

    url = "https://randomuser.me/api/?nat=us,au,gb&results=" + str(number)
    response = requests.get(url).text
    random_users = json.loads(response)

    for random_user in random_users['results']:

        username = random_user['login']['password']
        email = random_user['email']
        password = random_user['login']['salt']
        icon = "static/icons/" + username + ".jpg"
        location = random_user['location']['city']

        url = 'https://dog.ceo/api/breeds/image/random'
        response = requests.get(url).text
        image_url = json.loads(response)
        image_url = image_url['message']
        urllib.request.urlretrieve(image_url, icon)

        user = User.objects.create_user(username, email, password)
        profile = Profile.objects.create(user=user)
        icon_file = Path( os.path.join(settings.BASE_DIR, 'static', 'icons', username + ".jpg"))
        if icon_file.is_file():
            profile.icon = icon
        profile.location = location
        profile.save()

    return HttpResponse('Done')