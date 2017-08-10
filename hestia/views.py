from django.contrib.auth import views as auth_views
from django.shortcuts import get_object_or_404, render

def home(request):
       return render(request, 'home.html')