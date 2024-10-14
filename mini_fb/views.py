#mini_fb/urls.py
# views to show the mini_fb application

from django.shortcuts import render

from . models import * 
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# class-based view
class ShowAllProfilesView(ListView):
    '''A view to show all Profiles.'''

    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

class ShowProfilePageView(DetailView):
    '''View to display a single Profile record.'''
    model = Profile
    template_name = 'mini_fb/show_profile_page.html'
    context_object_name = 'profile'