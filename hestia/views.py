from django.contrib.auth import views as auth_views
from django.shortcuts import get_object_or_404, render
from django.db.models import Count, Min

from forums.models import Thread, Response
from django.contrib.auth.models import User

def home(request):
   return render(request, 'home.html')

def about(request):

	first_thread_date = Thread.objects.all().aggregate(Min('thread_date'))
	number_of_users = User.objects.count()
	newest_user = User.objects.order_by('-date_joined').first()
	number_of_posts = Thread.objects.count() + Response.objects.count()
	# popular_thread = Thread.objects.annotate(responses=response_set.count()).order_by('-responses')

	popular_thread = Thread.objects.annotate(num_replies=Count('response')).order_by('-num_replies').first()
	top_poster = User.objects.annotate(num_replies=Count('response')).order_by('-num_replies').first()
	post_rankings = User.objects.annotate(num_replies=Count('response')).order_by('-num_replies')[:5]


	data = {
		'first_thread_date': first_thread_date,
		'number_of_users': number_of_users,
		'newest_user': newest_user,
		'number_of_posts': number_of_posts,
		'popular_thread': popular_thread,
		'top_poster': top_poster,
		'post_rankings': post_rankings
	}
	return render(request, 'about.html', data)