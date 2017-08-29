from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone

from .models import Group
from django.contrib.auth.models import User

def new(request):
    if request.method == "POST":
        name = request.POST['name']
        description = request.POST['description']
        created = timezone.now()
        if request.user.is_authenticated():
            user = request.user
        group = Group(name=name, description=description, created=created, owner=user)
        group.save()
        if group is not None:
            return HttpResponseRedirect('/groups/' + str(group.id))
        else:
            messages.error(request, 'Bad.')
        return render(request, 'groups/new.html')
    else:
        return render(request, 'groups/new.html')