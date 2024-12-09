from django import forms
from .models import *

class CreatePlayerForm(forms.ModelForm):

    POSITTION_CHOICES = (
        ('ND','Not Determined'),
        ('S','Setter '),
        ('MB','Middle Blocker'),
        ('L','Libero'),
        ('OH', 'Outside Hitter'),
        ('OP', 'Opposite Hitter'),
        ('DS', 'Defensive Specialist')
    )
    first_name = forms.CharField(label="First Name", required=True)
    last_name = forms.CharField(label="Last Name", required=True)
    position = models.CharField(max_length=2, choices=POSITTION_CHOICES, default='ND')
    number = forms.IntegerField(label="Number", required=True)
    profile_image_file = forms.ImageField(label="Profile Image", required=False)


    class Meta:
        '''associate this form with the Profile model'''
        model = Player
        fields = ['first_name', 'last_name', 'position', 'number', 'profile_image_file']

class CreateManagerForm(forms.ModelForm):
    first_name = forms.CharField(label="First Name", required=True)
    last_name = forms.CharField(label="Last Name", required=True)
    email = forms.EmailField(label="Email", required=True)

    class Meta:
        '''Associate this form with the Manager model.'''
        model = Manager
        fields = ['first_name', 'last_name', 'email']


class CreateTeamForm(forms.ModelForm):
    name = forms.CharField(label="Team Name", required=True)
    city = forms.CharField(label="City", required=True)
    country = forms.CharField(label="Country", required=True)

    class Meta:
        '''Associate this form with the Team model.'''
        model = Team
        fields = ['name', 'city', 'country']

class CreateMatchRequestForm(forms.ModelForm):
    date = forms.DateField(
        label="Match Date",
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True,
        help_text="Choose a future date for the match."
    )

    class Meta:
        model = MatchRequest
        fields = ['date']

class UpdatePlayerForm(forms.ModelForm):
    POSITTION_CHOICES = (
        ('ND', 'Not Determined'),
        ('S', 'Setter'),
        ('MB', 'Middle Blocker'),
        ('L', 'Libero'),
        ('OH', 'Outside Hitter'),
        ('OP', 'Opposite Hitter'),
        ('DS', 'Defensive Specialist')
    )
    
    first_name = forms.CharField(label="First Name", required=True)
    last_name = forms.CharField(label="Last Name", required=True)
    position = forms.ChoiceField(choices=POSITTION_CHOICES, required=True)
    number = forms.IntegerField(label="Number", required=True)
    profile_image_file = forms.ImageField(label="Profile Image", required=False)

    class Meta:
        model = Player
        fields = ['first_name', 'last_name', 'position', 'number', 'profile_image_file']


class UpdateManagerForm(forms.ModelForm):
    first_name = forms.CharField(label="First Name", required=True)
    last_name = forms.CharField(label="Last Name", required=True)
    email = forms.EmailField(label="Email", required=True)
    profile_image_file = forms.ImageField(label="Profile Image", required=False)

    class Meta:
        model = Manager
        fields = ['first_name', 'last_name', 'email', 'profile_image_file']