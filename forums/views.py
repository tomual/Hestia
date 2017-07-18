from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from datetime import date
from .models import Thread

def index(request):
    latest_thread_list = Thread.objects.order_by('-thread_date')[:5]
    context = {
        'latest_thread_list': latest_thread_list,
    }
    return render(request, 'forums/index.html', context)

def view(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    context = {
        'thread': thread,
    }
    return render(request, 'forums/view.html', context)

def respond(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    response = thread.response_set.create(response_content = request.POST.get('response_content'), response_date = date.today())
    response.save()
    return HttpResponseRedirect('/forums/' + thread_id)