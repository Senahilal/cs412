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
    
    def get_friends(self):
        '''List of Profiles that are friends with this Profile.'''
        friends = Friend.objects.filter(models.Q(profile1=self) | models.Q(profile2=self))
        friend_profiles = []

        for friend in friends:
            if friend.profile1 == self:
                friend_profiles.append(friend.profile2)
            else:
                friend_profiles.append(friend.profile1)

        return friend_profiles

    def add_friend(self, other):
        '''Add a Friend relation between self and other'''

        # Check if the other profile exists
        if not isinstance(other, Profile):
            return "Invalid profile object."
        
        # Check for self-friending
        if self == other:
            return "Cannot add self as friend."

        # Check if a friendship already exists in either direction
        friendship_exists = Friend.objects.filter(models.Q(profile1=self, profile2=other) | models.Q(profile1=other, profile2=self)).exists()

        if not friendship_exists:
            # Create a new Friend instance and save
            new_friendship = Friend(profile1=self, profile2=other)
            new_friendship.save()
            return "Friend added successfully."
        return "Friendship already exists."

    def get_friend_suggestions(self):
        # Get all profiles except self
        all_profiles = Profile.objects.exclude(pk=self.pk)
        
        # Filter profiles not in current friends list
        current_friends = self.get_friends()
        suggestions = all_profiles.exclude(pk__in=[friend.pk for friend in current_friends])
        
        return suggestions


class StatusMessage(models.Model):
    '''Encapsulate the data for a status message.'''

    timestamp = models.DateTimeField(default=datetime.now)
    message = models.TextField(blank=False)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)

    def __str__(self):
        '''String representation of the object'''
        return f"{self.message}"
    
    def get_images(self):
        '''Return all images of this status message.'''
        return Image.objects.filter(status_message=self)
    
class Image(models.Model):
    '''Encapsulate the data for an uploaded image file.'''
    
    image_file = models.ImageField(blank=False) #If they didnt uplaod any file, there is no meaning to create Image object
    timestamp = models.DateTimeField(default=datetime.now)  # Timestamp when the image is uploaded
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)

    def __str__(self):
        '''Return a string representation of this Image.'''
        return f"Image for {self.status_message}"

class Friend(models.Model):
    '''Represents a friendship relation between two profiles.'''

    profile1 = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name="profile1")
    profile2 = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name="profile2")
    timestamp = models.DateTimeField(default=datetime.now) #timestamp of the friendship creation (i.e., “anniversary”) date

    def __str__(self):
        '''Relationship as a string representation.'''
        return f"{self.profile1.first_name} {self.profile1.last_name} & {self.profile2.first_name} {self.profile2.last_name}"