#mini_fb/views.py
# views to show the mini_fb application
from typing import Any
from django.shortcuts import render, redirect
from django.urls import reverse

from . models import *
from . forms import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.shortcuts import redirect, get_object_or_404

from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.forms import UserCreationForm ## NEW
from django.contrib.auth.models import User ## NEW
from django.contrib.auth import login ## NEW

# class-based view
class ShowAllProfilesView(ListView):
    '''A view to show all Profiles.'''

    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

class ShowProfilePageView(DetailView):
    '''View to display a single Profile record.'''
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'

class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def get_success_url(self):
        '''Redirect to the profile page after posting a status.'''
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        '''Attach the status message to the correct profile.'''

        # find the profile with the PK from the URL
        # self.kwargs['pk'] is finding the profile PK from the URL
        profile = Profile.objects.get(pk=self.kwargs['pk'])

        # attach the profile to the new Status 
        # (form.instance is the new Status object)
        form.instance.profile = profile

        # save the status message to database
        sm = form.save()

        # read the file from the form:
        files = self.request.FILES.getlist('files')

        for file in files:
            image = Image()
            image.image_file = file    # Set the image file
            image.status_message = sm  # Link to the status message
            image.save()               # Save the image object

        # delegate work to the superclass version of this method
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''Add the profile object to the context.'''

        # get the super class version of context data
        context = super().get_context_data(**kwargs)

        # find the profile with the PK from the URL
        # self.kwargs['pk'] is finding the profile PK from the URL
        profile = Profile.objects.get(pk=self.kwargs['pk'])

        # add the profile to the context data
        context['profile'] = profile  # Add it to the context
        return context

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_success_url(self):
        '''Redirect to the profile page after updating a profile.'''
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})

class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status'

    def get_success_url(self):
        '''Redirect to the profile page after deleting the status message'''
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/update_status_form.html'
    context_object_name = 'status'

    def get_success_url(self):
        '''Redirect to the profile page after updating a status message.'''
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

class CreateFriendView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):

        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            return self.handle_no_permission()  # Redirects to login page if user is not authenticated
        
        # Get the profiles involved in the friendship
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        other_profile = Profile.objects.get(pk=self.kwargs['other_pk'])
        
        # Add the friend
        profile.add_friend(other_profile)
        
        # Redirect back to the profile page
        return redirect('show_profile', pk=profile.pk)

class ShowFriendSuggestionsView(DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['friend_suggestions'] = self.object.get_friend_suggestions()
        return context

class ShowNewsFeedView(DetailView):
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_feed'] = self.object.get_news_feed()
        return context