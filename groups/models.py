from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime

class Group(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    created = models.DateTimeField('date created')
    icon = models.ImageField(upload_to='static/group_icons', default='static/group_icons/aurora2.png')
    members = models.ManyToManyField(User, through='Membership')

    def __str__(self):
    	return self.name

class Membership(models.Model):
	user = models.ForeignKey(User)
	group = models.ForeignKey(Group)
	joined = models.DateTimeField('date joined',default=datetime.now, blank=True)
	owner = models.BooleanField(default=False)