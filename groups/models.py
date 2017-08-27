from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Group(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    created = models.DateTimeField('date created')
    icon = models.ImageField(upload_to='static/group_icons', blank=True)

    def __str__(self):
    	return self.name
