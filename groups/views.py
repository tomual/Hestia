from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone

from .models import Group, Membership
from .forms import GroupForm
from django.contrib.auth.models import User

def index(request):
    groups = Group.objects.all()
    return render(request, 'groups/index.html', {'groups':groups})

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
            name = request.POST['name']
            description = request.POST['description']
            created = timezone.now()
            group = Group(name=name, description=description, created=created, icon=form.cleaned_data['icon'])
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
            group.description = request.POST['description']
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
