from django.db import models
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Player(models.Model):
    POSITTION_CHOICES = (
        ('ND','Not Determined'),
        ('S','Setter '),
        ('MB','Middle Blocker'),
        ('L','Libero'),
        ('OH', 'Outside Hitter'),
        ('OP', 'Opposite Hitter'),
        ('DS', 'Defensive Specialist')
    )
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.CharField(max_length=2, choices=POSITTION_CHOICES, default='ND')
    number = models.IntegerField(blank=True, null=True)
    profile_image_file = models.ImageField(blank=True, null=True)
    

    #associate each Player with an User for authentication and identification purposes
    #, null=True, blank=True
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # Link to Django User


    def __str__(self):
        return f"{self.first_name} {self.last_name}"

#Manager / head coach of the team
class Manager(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    is_approved = models.BooleanField(default=False)
    profile_image_file = models.ImageField(blank=True, null=True)

    #associate each Manager with an User for authentication and identification purposes
    #, null=True, blank=True
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # Link to Django User

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Team(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Match(models.Model):
    date = models.DateField()
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_team')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_team')
    home_score = models.IntegerField()
    away_score = models.IntegerField()
    
    def __str__(self):
        return f"{self.home_team} vs {self.away_team} on {self.date}"


class PlaysIn(models.Model):
    '''Represents a relation between a team and a player.'''
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True) #null when player is currently in the team

    def __str__(self):
        #If player is not playing in this team anymore
        if self.end_date:
            return f"{self.player} played in {self.team} from {self.start_date} to {self.end_date}"
        else:
            return f"{self.player} plays in {self.team}" #player is currently playing in this team