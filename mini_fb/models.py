from django.db import models
from datetime import datetime
from django.urls import reverse

#This Profile model includes the following data attributes: first name, last name, city, email address, and a profile image url.

# Create your models here.
class Profile(models.Model):
    '''Encapsulate the data for an user profile.'''

    # data attributes:
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.TextField(blank=False)
    image_url = models.URLField(blank=True) 

    def __str__(self):
        '''Return a string representation of this Profile.'''
        return f"{self.first_name} {self.last_name}"
    
    def get_status_messages(self):
        '''Get all status messages for this profile, ordered by timestamp.'''
        return StatusMessage.objects.filter(profile=self).order_by('-timestamp')
    
    def get_absolute_url(self):
        '''Return a URL to show this one profile'''
        return reverse('show_profile', kwargs={'pk': self.pk})


class StatusMessage(models.Model):
    '''Encapsulate the data for a status message.'''

    timestamp = models.DateTimeField(default=datetime.now)
    message = models.TextField(blank=False)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)

    def __str__(self):
        '''String representation of the object'''
        return f"{self.message}"