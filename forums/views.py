from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.views import generic
from datetime import datetime
from django.utils import timezone
from django.db.models import Count, Max, Case, When, Value, DateField, IntegerField, DateTimeField

from .models import Thread, Response
from django.contrib.auth.models import User
from .forms import ThreadForm, ResponseForm

class IndexView(generic.ListView):
    template_name = 'forums/index.html'
    context_object_name = 'latest_thread_list'

    def get_queryset(self):
        return Thread.objects.annotate(num_responses=Count('response')).annotate(recent_response=Max('response__posted')).annotate(test=Max('response__posted'))


def view(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    form = ResponseForm()
    return render(request, 'forums/view.html', {'thread':thread, 'form': form})

def respond(request, thread_id):    
    thread = get_object_or_404(Thread, pk=thread_id)
    if request.method == "POST":
        form = ResponseForm(request.POST, request.FILES)
        if form.is_valid():
            if request.user.is_authenticated():
                user = request.user
            response = thread.response_set.create(message = request.POST.get('message'), posted = datetime.now(), poster = user)

            response.save()
            return HttpResponseRedirect('/forums/' + thread_id)
        else:
            return render(request, 'forums/respond.html', {'thread':thread, 'form': form})
    else:
        form = ResponseForm()
        return render(request, 'forums/respond.html', {'thread':thread, 'form': form})

def new(request):
    if request.method == "POST":
        title = request.POST['title']
        message = request.POST['message']
        posted = timezone.now()
        form = ThreadForm(request.POST, request.FILES)
        if form.is_valid():            
            if request.user.is_authenticated():
                user = request.user
            thread = Thread(title=title, message=message, posted=posted, poster=user)
            thread.save()
            if thread is not None:
                return HttpResponseRedirect('/forums/' + str(thread.id))
        return render(request, 'forums/new.html', {'form': form})
    else:
        form = ThreadForm()
        return render(request, 'forums/new.html', {'form': form})