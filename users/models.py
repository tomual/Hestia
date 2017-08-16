from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):  
    user = models.OneToOneField(User)
    location = models.CharField(max_length=140, blank=True)
    description = models.CharField(max_length=255, blank=True)
    icon = models.ImageField(upload_to='icons', blank=True)

    def __unicode__(self):
        return u'Profile of user: %s' % self.user.username