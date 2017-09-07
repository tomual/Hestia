from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission, User
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from .forms import UserForm, LoginForm, RegisterForm

def index(request):
    users = User.objects.all()
    return render(request, 'users/index.html', {'users':users})

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