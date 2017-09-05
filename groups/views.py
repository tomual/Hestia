from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone

from .models import Group, Membership
from .forms import ImageUploader
from django.contrib.auth.models import User

def index(request):
    groups = Group.objects.all()
    return render(request, 'groups/index.html', {'groups':groups})

def view(request, id):
    group = Group.objects.get(id=id)
    try:
        membership = group.membership_set.get(user=request.user)
    except Membership.DoesNotExist:
        membership = False
    return render(request, 'groups/view.html', {'group':group, 'membership':membership})

def new(request):
    if request.method == "POST":
        name = request.POST['name']
        description = request.POST['description']
        created = timezone.now()
        if request.user.is_authenticated():
            user = request.user
        group = Group(name=name, description=description, created=created)
        group.save()
        if group is not None:
            Membership.objects.create(user=user,group=group, owner=True)
            return HttpResponseRedirect('/groups/' + str(group.id))
        else:
            messages.error(request, 'Bad.')
        return render(request, 'groups/new.html')
    else:
        return render(request, 'groups/new.html')

def edit(request, id):
    group = Group.objects.get(id=id)
    if request.method == "POST":
        group.description = request.POST['description']

        if request.FILES.get('icon', False):
            form = ImageUploader(request.POST, request.FILES)
            if form.is_valid():
                group.icon = form.cleaned_data['icon']

        group.save()

        return render(request, 'groups/edit.html', {'group':group})
    else:
        return render(request, 'groups/edit.html', {'group':group})

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
