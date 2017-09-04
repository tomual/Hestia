from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission, User
from django.contrib import messages

def index(request):
    users = User.objects.all()
    return render(request, 'users/index.html', {'users':users})

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

def profile(request, username):
    profile_user = User.objects.get(username=username)
    return render(request, 'users/profile.html', {'profile_user':profile_user})

def edit(request):
    if request.method == "POST":
        user_edit = User.objects.get(username=request.user.username)
        user_edit.email = request.POST['email']
        user_edit.profile.location = request.POST['location']
        user_edit.profile.description = request.POST['description']
        user_edit.profile.save()
        user_edit.save()
        return render(request, 'users/edit.html')
    else:
        return render(request, 'users/edit.html')