from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission, User
from django.contrib import messages

def index(request):
    return render(request, 'users/index.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.error(request, 'Yay.')
        else:
            messages.error(request, 'Invalid login.')
        return render(request, 'users/login.html')
    else:
        return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    return redirect('/')

def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username, email, password)
        if user is not None:
            login(request, user)
            messages.error(request, 'Yay.')
        else:
            messages.error(request, 'Invalid login.')
        return render(request, 'users/register.html')
    else:
        return render(request, 'users/register.html')