from datetime import datetime

from forums.models import Thread, Response
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse

class CheckLoggedInMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated():
            if request.get_full_path() != '/top' and request.get_full_path() != '/users/login'and request.get_full_path() != '/users/register':
                return redirect('/top')

        response = self.get_response(request)
        return response