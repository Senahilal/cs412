#mini_fb/views.py
# views to show the mini_fb application
from typing import Any
from django.shortcuts import render
from django.urls import reverse

from . models import *
from . forms import *
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
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'

class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

class CreateStatusMessageView(CreateView):
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

class UpdateProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_success_url(self):
        '''Redirect to the profile page after updating a profile.'''
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})

class DeleteStatusMessageView(DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status'

    def get_success_url(self):
        '''Redirect to the profile page after deleting the status message'''
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

class UpdateStatusMessageView(UpdateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/update_status_form.html'
    context_object_name = 'status'

    def get_success_url(self):
        '''Redirect to the profile page after updating a status message.'''
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})