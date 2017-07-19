from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.views import generic
from datetime import date

from .models import Thread, Response

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
    response = thread.response_set.create(response_content = request.POST.get('response_content'), response_date = date.today())
    response.save()
    return HttpResponseRedirect('/forums/' + thread_id)