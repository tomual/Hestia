import random
import requests
import urllib.request
import os.path
import bleach

from pathlib import Path
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone

from .models import Group, Membership
from .forms import GroupForm
from django.contrib.auth.models import User

def index(request):
    groups_all = Group.objects.all()

    paginator = Paginator(groups_all, 10)
    page = request.GET.get('page')
    try:
        groups = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        groups = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        groups = paginator.page(paginator.num_pages)
    page_numbers = range(1, paginator.num_pages + 1)

    return render(request, 'groups/index.html', {'groups':groups, 'page_numbers':page_numbers})

def view(request, id):
    group = Group.objects.get(id=id)
    members = group.membership_set.all()

    try:
        owner = Membership.objects.get(group=group, owner=True)
    except Membership.DoesNotExist:
        owner = 'Nobody'

    try:
        membership = group.membership_set.get(user=request.user)
    except Membership.DoesNotExist:
        membership = None
    return render(request, 'groups/view.html', {'group':group, 'membership':membership, 'owner':owner, 'members':members})

def new(request):
    if request.method == "POST":
        form = GroupForm(request.POST, request.FILES)
        if form.is_valid():
            if request.user.is_authenticated():
                user = request.user
            name = form.cleaned_data['name']
            description = bleach.clean(form.cleaned_data['description'], settings.ALLOWED_TAGS, strip=True)
            created = timezone.now()
            group = Group(name=name, description=description, created=created)
            if request.FILES.get('icon', False):
                group.icon = form.cleaned_data['icon']
            group.save()
            if group is not None:
                Membership.objects.create(user=user,group=group, owner=True)
                return HttpResponseRedirect('/groups/' + str(group.id))

        return render(request, 'groups/new.html', {'form':form})
    else:
        form = GroupForm()
        return render(request, 'groups/new.html', {'form':form})

def edit(request, id):
    group = Group.objects.get(id=id)
    if request.method == "POST":
        form = GroupForm(request.POST, request.FILES)
        if form.is_valid():
            if request.FILES.get('icon', False):
                group.icon = form.cleaned_data['icon']
            group.description = bleach.clean(form.cleaned_data['description'], settings.ALLOWED_TAGS, strip=True)
            group.save()
        return render(request, 'groups/edit.html', {'group':group, 'form':form})
    else:
        data = {
            'name': group.name,
            'description': group.description,
        }
        form = GroupForm(initial=data)
        return render(request, 'groups/edit.html', {'group':group, 'form':form})

def join(request, id):
    group = Group.objects.get(id=id)
    Membership.objects.create(user=request.user,group=group)
    return HttpResponseRedirect('/groups/' + str(group.id))

def leave(request, id):
    group = Group.objects.get(id=id)
    try:
        group.membership_set.get(user=request.user).delete()
    except Membership.DoesNotExist:
        pass
    return HttpResponseRedirect('/groups/' + str(group.id))

def generate_groups(request):
    groups_start = [
        'The',
        'Only',
        'Members of',
        'People who like',
        'Many',
        'Group for'
    ]

    for x in range(0, 30):
        url = "http://setgetgo.com/randomword/get.php"
        word = requests.get(url).text.capitalize()

        url = 'http://dinoipsum.herokuapp.com/api/?format=html&paragraphs=3&words=15'
        description = requests.get(url).text

        name = random.choice(groups_start) + ' ' + word
        user = random.choice(User.objects.all())
        created = timezone.now()
        icon = "static/group_icons/" + name + ".jpg"

        url = 'http://lorempixel.com/400/200/'
        urllib.request.urlretrieve(url, icon)

        group = Group(name=name, description=description, created=created)
        group.save()
        if group is not None:
            Membership.objects.create(user=user,group=group, owner=True)

        icon_file = Path( os.path.join(settings.BASE_DIR, 'static', 'group_icons', name + ".jpg"))
        if icon_file.is_file():
            group.icon = icon
        group.save()


    return HttpResponse('Done')