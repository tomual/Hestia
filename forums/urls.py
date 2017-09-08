from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # /thread/5/
    url(r'^(?P<thread_id>[0-9]+)/$', views.view, name='view'),
    # /thread/5/respond/
    url(r'^(?P<thread_id>[0-9]+)/respond/$', views.respond, name='respond'),
    url(r'^new$', views.new, name='new'),
]