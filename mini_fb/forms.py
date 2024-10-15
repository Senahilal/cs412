from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    
    first_name = forms.CharField(label="First Name", required=True)
    last_name = forms.CharField(label="Last Name", required=True)
    city = forms.CharField(label="City", required=True)
    email = forms.CharField(label="Email", required=True)

    class Meta:
        '''associate this form witht he Profile model'''
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email', 'image_url']

class CreateStatusMessageForm(forms.ModelForm):
    message = forms.CharField(label="Message", required=True)
    class Meta:
        model = StatusMessage
        fields = ['message']