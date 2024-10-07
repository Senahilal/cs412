#mini_fb/urls.py
# views to show the mini_fb application

from django.shortcuts import render

from . models import * 
from django.views.generic import ListView

# class-based view
class ShowAllProfilesView(ListView):
    '''A view to show all Articles.'''

    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'