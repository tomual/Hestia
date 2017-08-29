from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<id>[0-9]+)$', views.view, name='view'),
    url(r'^new$', views.new, name='new'),
]