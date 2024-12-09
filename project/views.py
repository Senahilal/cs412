from typing import Any
from django.shortcuts import render, redirect
from django.urls import reverse

from . models import *
from . forms import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.shortcuts import redirect, get_object_or_404

from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User 
from django.contrib.auth import login
from django.contrib import messages


# Create your views here.
class ShowAllMatchesView(ListView):
    '''A view to show all Matxhes.'''

    model = Match
    template_name = 'project/show_all_matches.html'
    context_object_name = 'matches'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['played_matches'] = Match.get_all_played_matches()
        context['scheduled_matches'] = Match.get_all_scheduled_matches()
        return context

class ShowAllTeamsView(ListView):
    '''A view to show all Matxhes.'''

    model = Team
    template_name = 'project/show_all_teams.html'
    context_object_name = 'teams'

    def get_queryset(self):
        """
        Ranks teams based on their standings data, specifically points and games played.
        """
        # Start with the base queryset of teams
        qs = super().get_queryset()

        # Calculating standings for each team
        standings = []
        for team in qs:
            data = team.get_standings_data()
            standings.append({
                "team": team,
                "games_played": data["games_played"],
                "wins": data["wins"],
                "losses": data["losses"],
                "draws": data["draws"],
                "points": data["points"],
                "sets_won": data["sets_won"],
            })

        # Sort teams primarily by points (descending)
        #  then by games played (ascending)
        qs = sorted(standings, key=lambda x: (-x["points"], x["games_played"]))

        # Return the sorted list of teams
        return qs

class ShowTeamPageView(DetailView):
    '''A view to show a single team.'''

    model = Team
    template_name = 'project/show_team_page.html'
    context_object_name = 'team'

    def get_context_data(self, **kwargs):
        '''Add additional context if needed.'''
        context = super().get_context_data(**kwargs)
        # Add any additional data to context
        team = self.get_object()
        context['standings_data'] = team.get_standings_data()

        return context

class ShowPlayerPageView(DetailView):
    '''A view to show a single player's profile.'''

    model = Player
    template_name = 'project/show_player.html'
    context_object_name = 'player'

    def get_context_data(self, **kwargs):
        '''Add additional context if needed.'''
        context = super().get_context_data(**kwargs)
        # Add any additional data to context

        return context

class ShowManagerPageView(DetailView):
    '''A view to show a single manager's profile.'''

    model = Manager
    template_name = 'project/show_manager.html'
    context_object_name = 'manager'

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
        context['create_team_form'] = CreateTeamForm()
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


            # Saving team instance with the manager

            team_form = CreateTeamForm(self.request.POST)
            if team_form.is_valid():
                team = team_form.save(commit=False)
                team.manager = self.object
                team.save()

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

# To update player information
class UpdatePlayerView(LoginRequiredMixin, UpdateView):
    model = Player
    form_class = UpdatePlayerForm
    template_name = 'project/update_player_form.html'

    # Redirect users to project_login if not authenticated
    def get_login_url(self):
        return reverse('project_login')

    def get_success_url(self):
        return reverse('show_player', kwargs={'pk': self.object.pk})

    # get the logged-in user
    def get_object(self):
        return self.request.user.player

# To update manager information
class UpdateManagerView(LoginRequiredMixin, UpdateView):
    model = Manager
    form_class = UpdateManagerForm
    template_name = 'project/update_manager_form.html'

    # Redirect users to project_login if not authenticated
    def get_login_url(self):
        return reverse('project_login')

    def get_success_url(self):
        return reverse('show_manager', kwargs={'pk': self.object.pk})

    # get the logged-in user
    def get_object(self):
        return self.request.user.manager  

# To show invitation and responses to player and manager profiles
class InboxView(LoginRequiredMixin, ListView):
    template_name = 'project/inbox.html'
    context_object_name = 'invitations'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if hasattr(user, 'manager'):
            context['received_requests'] = MatchRequest.objects.filter(receiver=user.manager).order_by('-timestamp')
            context['sent_requests'] = MatchRequest.objects.filter(sender=user.manager).order_by('-timestamp')
        
        return context

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'player'):  # Player's inbox
            return Invitation.objects.filter(invitee=user.player).order_by('-timestamp')
        elif hasattr(user, 'manager'):  # Manager's sent invitations
            return Invitation.objects.filter(inviter=user.manager).order_by('-timestamp')
        return Invitation.objects.none()
    
    # Redirect users to project_login if not authenticated
    def get_login_url(self):
        return reverse('project_login')


class SendInvitationView(LoginRequiredMixin, View):
    
    # Redirect users to project_login if not authenticated
    def get_login_url(self):
        return reverse('project_login')
    
    def dispatch(self, request, *args, **kwargs):
        # Ensure the user is a manager
        if not hasattr(request.user, 'manager'):
            messages.error(request, "Only managers can send invitations.")
            return redirect('show_player', pk=self.kwargs['player_pk'])

        manager = request.user.manager
        player = get_object_or_404(Player, pk=self.kwargs['player_pk'])

        try:
            # Use the method in manager model to send the invitation
            message = manager.send_invitation(player)
            messages.success(request, message)
        except ValueError as e:
            messages.error(request, str(e))

        return redirect('show_player', pk=player.pk)

class RespondInvitationView(LoginRequiredMixin, View):
    
    # Redirect users to project_login if not authenticated
    def get_login_url(self):
        return reverse('project_login')

    def dispatch(self, request, *args, **kwargs):
        # Ensure the user is a player
        if not hasattr(request.user, 'player'):
            messages.error(request, "Only players can respond to invitations.")
            return redirect('inbox')

        player = request.user.player
        invitation = get_object_or_404(Invitation, pk=self.kwargs['invite_pk'], invitee=player)

        if request.method == 'POST':
            response = request.POST.get('response')
            try:
                # Use the method in player model to respond to the invitation
                message = player.respond_to_invitation(invitation, response)
                messages.success(request, message)
            except ValueError as e:
                messages.error(request, str(e))

        return redirect('inbox')

class SendMatchRequestView(LoginRequiredMixin, CreateView):
    model = MatchRequest
    form_class = CreateMatchRequestForm
    template_name = 'project/send_match_request.html'

    def get_success_url(self):
        """Redirect back to the team's page after a successful match request."""
        return reverse('show_team', kwargs={'pk': self.kwargs['team_pk']})

    def form_valid(self, form):
        """Attach the sender and receiver managers to the match request."""
        # Ensure the user is a manager
        if not hasattr(self.request.user, 'manager'):
            messages.error(self.request, "Only managers can send match requests.")
            return redirect('show_team', pk=self.kwargs['team_pk'])

        sender_manager = self.request.user.manager  # Sender is the current user's manager
        receiver_team = get_object_or_404(Team, pk=self.kwargs['team_pk'])  # Team to which the request is being sent
        receiver_manager = receiver_team.manager  # Receiver is the team's manager

        # Validate the match date
        date = form.cleaned_data['date']
        if date <= datetime.now().date():
            form.add_error('date', "The match date must be in the future.")
            return self.form_invalid(form)

        # Check for existing requests for the same date
        existing_request = MatchRequest.objects.filter(
            sender=sender_manager,
            receiver=receiver_manager,
            date=date,
        ).first()

        if existing_request:
            messages.error(self.request, "A match request is already pending.")
            return redirect('show_team', pk=self.kwargs['team_pk'])

        # Attach sender, receiver, and date to the match request
        form.instance.sender = sender_manager
        form.instance.receiver = receiver_manager

        messages.success(self.request, "Match request sent successfully.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Add the team to the context."""
        context = super().get_context_data(**kwargs)
        context['team'] = get_object_or_404(Team, pk=self.kwargs['team_pk'])
        return context

class RespondMatchRequestView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        # Ensure the user is a manager
        if not hasattr(request.user, 'manager'):
            messages.error(request, "Only managers can respond to match requests.")
            return redirect('inbox')

        match_request = get_object_or_404(MatchRequest, pk=self.kwargs['match_request_pk'])

        if request.method == 'POST':
            response = request.POST.get('response')  # 'Accepted' or 'Rejected'
            try:
                # Use the method in the manager model to respond to the match request
                message = request.user.manager.respond_to_match_request(match_request, response)
                messages.success(request, message)
            except ValueError as e:
                messages.error(request, str(e))

        return redirect('inbox')

