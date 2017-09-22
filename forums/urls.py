from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new$', views.new, name='new'),
    url(r'^(?P<thread_id>[0-9]+)/$', views.view, name='view'),
    url(r'^(?P<thread_id>[0-9]+)/respond/$', views.respond, name='respond'),
]