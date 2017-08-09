from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.views import generic
from datetime import date
from django.utils import timezone

from .models import Thread, Response
from django.contrib.auth.models import User

class IndexView(generic.ListView):
    template_name = 'forums/index.html'
    context_object_name = 'latest_thread_list'

    def get_queryset(self):
        return Thread.objects.order_by('-thread_date')[:5]

class ViewView(generic.DetailView):
    model = Thread 
    template_name = 'forums/view.html'

def respond(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    if request.user.is_authenticated():
        user = request.user
    response = thread.response_set.create(response_content = request.POST.get('response_content'), response_date = date.today(), author = user)

    response.save()
    return HttpResponseRedirect('/forums/' + thread_id)

def new(request):
    if request.method == "POST":
        thread_title = request.POST['thread_title']
        thread_content = request.POST['thread_content']
        thread_date = timezone.now()
        if request.user.is_authenticated():
            user = request.user
        thread = Thread(thread_title=thread_title, thread_content=thread_content, thread_date=thread_date, author=user)
        thread.save()
        if thread is not None:
            return HttpResponseRedirect('/forums/' + str(thread.id))
        else:
            messages.error(request, 'Bad.')
        return render(request, 'forums/new.html')
    else:
        return render(request, 'forums/new.html')