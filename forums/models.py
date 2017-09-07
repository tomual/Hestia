import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Count, Max

class Thread(models.Model):
    title = models.CharField(max_length=200)
    message = models.CharField(max_length=200)
    posted = models.DateTimeField('date posted')
    poster = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)

    def __str__(self):
    	return self.title

    def was_posted_recently(self):
    	now = timezone.now()
    	return now - datetime.timedelta(days=1) <= self.posted <= now

    was_posted_recently.posted  = True
    was_posted_recently.boolean = True
    was_posted_recently.short_description = 'Published recently?'


class Response(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    poster = models.ForeignKey(settings.AUTH_USER_MODEL)
    message = models.CharField(max_length=200)
    posted = models.DateTimeField('date posted')

    def __str__(self):
    	return self.message[:10]