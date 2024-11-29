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

# Create your views here.
class ShowAllMatchesView(ListView):
    '''A view to show all Matxhes.'''

    model = Match
    template_name = 'project/show_all_matches.html'
    context_object_name = 'matches'

class ShowAllTeamsView(ListView):
    '''A view to show all Matxhes.'''

    model = Team
    template_name = 'project/show_all_teams.html'
    context_object_name = 'teams'

class ShowTeamPageView(DetailView):
    '''A view to show a single team.'''

    model = Team
    template_name = 'project/show_team_page.html'
    context_object_name = 'team'

    def get_context_data(self, **kwargs):
        '''Add players to the context for display in the template.'''
        context = super().get_context_data(**kwargs)
        team = self.get_object()

        # Fetch players associated with this team using the PlaysIn model
        plays_in = PlaysIn.objects.filter(team=team).select_related('player')
        context['players'] = [play_in.player for play_in in plays_in]
        return context

class ShowPlayerPageView(DetailView):
    '''A view to show a single player's profile.'''

    model = Player
    template_name = 'project/show_player.html'
    context_object_name = 'player'

    def get_context_data(self, **kwargs):
        '''Add additional context if needed.'''
        context = super().get_context_data(**kwargs)
        # Add any additional data you'd like to include in the context
        return context

class CreatePlayerView(CreateView):
    '''A view to create a new profile.'''

    model = Player
    form_class = CreatePlayerForm
    template_name = 'project/create_player_form.html'

    def get_context_data(self, **kwargs: Any):
        '''Add both forms to the context for display in the template.'''

        context = super().get_context_data(**kwargs)
        # Pass an unbound UserCreationForm instance to the template
        context['user_creation_form'] = UserCreationForm()

        return context

    def form_valid(self, form):
        '''Handle form submission for both Profile and UserCreationForm.'''
        # Recreate the UserCreationForm with POST data
        user_creation_form = UserCreationForm(self.request.POST)

        # Validate both forms
        if user_creation_form.is_valid():
            # Save the UserCreationForm to create a new user
            user = user_creation_form.save()

            # Attach the newly created user to the Player instance (form.instance)
            form.instance.user = user

            # Save the Player instance
            self.object = form.save()

            # Delegate the rest to the superclass
            return super().form_valid(form)
        else:
            # If user creation form is invalid, re-render with errors
            return self.form_invalid(form)

class CreateManagerView(CreateView):
    '''A view to create a new manager profile.'''

    model = Manager
    form_class = CreateManagerForm
    template_name = 'project/create_manager_form.html'

    def get_context_data(self, **kwargs: Any):
        '''Add both forms to the context for display in the template.'''

        context = super().get_context_data(**kwargs)
        # Pass an unbound UserCreationForm instance to the template
        context['user_creation_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        '''Handle form submission for both Manager and UserCreationForm.'''
        # Recreate the UserCreationForm with POST data
        user_creation_form = UserCreationForm(self.request.POST)

        # Validate both forms
        if user_creation_form.is_valid():
            # Save the UserCreationForm to create a new user
            user = user_creation_form.save()

            # Attach the newly created user to the Manager instance (form.instance)
            form.instance.user = user

            # Save the Manager instance
            self.object = form.save()

            # Delegate the rest to the superclass
            return super().form_valid(form)
        else:
            # If user creation form is invalid, re-render with errors
            return self.form_invalid(form)
    
    def get_success_url(self):
        '''Redirect to the team page of the created manager.'''
        team = Team.objects.filter(manager=self.object).first()
        if team:
            return reverse('show_team', kwargs={'pk': team.pk})
        return reverse('show_all_teams')  # Defaultm page to go to if no team is found