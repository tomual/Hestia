from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^profile/(?P<username>[A-z0-9]+)$', views.profile, name='profile'),
    url(r'^login$', views.login_view, name='login'),
    url(r'^logout$', views.logout_view, name='logout'),
    url(r'^register$', views.register_view, name='register'),
    url(r'^edit$', views.edit, name='edit'),
    url(r'^generate_users$', views.generate_users, name='generate_users'),
]