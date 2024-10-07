from django.db import models

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