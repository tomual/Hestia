import datetime

from django.db import models
from django.utils import timezone

class Thread(models.Model):
    thread_title = models.CharField(max_length=200)
    thread_content = models.CharField(max_length=200)
    thread_date = models.DateTimeField('date posted')

    def __str__(self):
    	return self.thread_title

    def was_posted_recently(self):
    	now = timezone.now()
    	return now - datetime.timedelta(days=1) <= self.thread_date <= now

    was_posted_recently.thread_date  = True
    was_posted_recently.boolean = True
    was_posted_recently.short_description = 'Published recently?'


class Response(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    response_content = models.CharField(max_length=200)
    response_date = models.DateTimeField('date posted')

    def __str__(self):
    	return self.response_content[:10]