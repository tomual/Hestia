import random
import requests

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.views import generic
from datetime import datetime
from django.utils import timezone
from django.db.models import Count, Max, Case, When, Value, DateField, IntegerField, DateTimeField
from django.db import connection
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Thread, Response
from django.contrib.auth.models import User
from .forms import ThreadForm, ResponseForm

def view(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    responses_all = thread.response_set.all()
    paginator = Paginator(responses_all, 15)
    page = request.GET.get('page')
    try:
        responses = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        if(page == 'last'):
            responses = paginator.page(paginator.num_pages)
        else:
            responses = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        responses = paginator.page(paginator.num_pages)
    form = ResponseForm()
    page_numbers = range(1, paginator.num_pages + 1)
    return render(request, 'forums/view.html', {'thread':thread, 'responses': responses, 'form': form, 'page_numbers': page_numbers})

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

    threads_all = threads

    paginator = Paginator(threads_all, 10)
    page = request.GET.get('page')
    try:
        threads = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        threads = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        threads = paginator.page(paginator.num_pages)
    form = ResponseForm()
    page_numbers = range(1, paginator.num_pages + 1)

    return render(request, 'forums/index.html', {'threads':threads, 'page_numbers':page_numbers})    

def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def randompost():
    bosses_start = [
        'I can\'t beat',
        'Can\'t seem to beat',
        'Having difficulty with',
        'Tips for',
        'Tips against',
        'How can I beat',
        'How do you take down',
        'How do you beat',
    ]
    bosses = [
        'Asylum Demon',
        'Bell Gargoyle',
        'Gargoyles',
        'Capra Demon',
        'Ceaseless Discharge',
        'Ceaseless',
        'Centipede Demon',
        'Chaos Witch Quelaag',
        'Crossbreed Priscilla',
        'Priscilla',
        'Dark Sun Gwyndolin',
        'Gwyndolin',
        'Demon Firesage',
        'Four Kings',
        '4K',
        'Gaping Dragon',
        'Sif',
        'Gwyn',
        'Iron Golem',
        'Moonlight Butterfly',
        'Nito',
        'Ornstein and Smough',
        'O&S',
        'Pinwheel',
        'Seath the Scaleless',
        'Seath',
        'Stray Demon',
        'Taurus Demon',
        'Bed of Chaos',
        'BoC',
    ]
    bosses_end = [
        '?',
        '!',
        ', help!',
        '??',
        '!!',
        '',
    ]
    url = 'http://dinoipsum.herokuapp.com/api/?format=html&paragraphs=3&words=15'
    message = requests.get(url)
    poster = random.choice(User.objects.all())
    title = random.choice(bosses_start) + ' ' + random.choice(bosses) + random.choice(bosses_end)
    posted = timezone.now()

    thread = Thread(title=title, message=message.text, posted=posted, poster=poster)
    thread.save()

    return thread

def randomreply():
    url = 'http://numbersapi.com/random/trivia'
    message = requests.get(url)
    poster = random.choice(User.objects.all())
    posted = timezone.now()

    # thread = Thread.objects.get(pk=106)
    # thread = random.choice(Thread.objects.all())

    response = thread.response_set.create(message = message.text, posted = datetime.now(), poster = poster)
    response.save()

    return response

def generate_posts(request):
    for x in range(0, 1):
        randompost()

    for x in range(0, 1):
        randomreply()

    return HttpResponse('Done')