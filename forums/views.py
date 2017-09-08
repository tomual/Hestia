from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.views import generic
from datetime import datetime
from django.utils import timezone
from django.db.models import Count, Max, Case, When, Value, DateField, IntegerField, DateTimeField
from django.db import connection


from .models import Thread, Response
from django.contrib.auth.models import User
from .forms import ThreadForm, ResponseForm

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

def index(request):
    sql = '''
        SELECT t.*,
           r.num_responses,
           tu.username AS thread_poster,
           ru.username AS response_poster,
           CASE
               WHEN r.posted IS NULL THEN t.posted
               ELSE r.posted
           END AS last_touch
        FROM forums_thread t
        LEFT JOIN
          (SELECT r.*,
                  COUNT(*) AS num_responses
           FROM forums_response r
           GROUP BY thread_id
           ORDER BY posted DESC) r ON t.id = thread_id
        LEFT JOIN
          (SELECT username,
                  id
           FROM auth_user) tu ON tu.id = t.poster_id
        LEFT JOIN
          (SELECT username,
                  id
           FROM auth_user) ru ON ru.id = r.poster_id
        ORDER BY last_touch DESC'''
    with connection.cursor() as cursor:
        cursor.execute(sql)
        threads = dictfetchall(cursor)

    for thread in threads:
        #raise Exception({thread['last_touch'],})
        try:
            thread['last_touch'] = datetime.strptime(thread['last_touch'], '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            thread['last_touch'] = datetime.strptime(thread['last_touch'], '%Y-%m-%d %H:%M:%S')
    return render(request, 'forums/index.html', {'threads':threads})    

def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]