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


# To show invitation and responses to player and manager profiles
class InboxView(LoginRequiredMixin, ListView):
    template_name = 'project/inbox.html'
    context_object_name = 'invitations'

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'player'):  # Player's inbox
            return Invitation.objects.filter(invitee=user.player).order_by('-timestamp')
        elif hasattr(user, 'manager'):  # Manager's sent invitations
            return Invitation.objects.filter(inviter=user.manager).order_by('-timestamp')
        return Invitation.objects.none()
    
    def get_login_url(self):
        return reverse('login')


# def send_invite(request, player_id):
#     """
#     Sends an invitation from the logged-in manager to the selected player.
#     """
#     # Get the player object by its ID
#     player = get_object_or_404(Player, id=player_id)
    
#     # Get the logged-in manager
#     manager = request.user.manager

#     # Check if the player is already in the manager's team
#     if player in manager.get_players_in_team():
#         messages.error(request, "Player is already in your team.")
#     else:
#         # Create a new invitation in the database
#         Invitation.objects.create(inviter=manager, invitee=player)
#         messages.success(request, f"Invitation sent to {player.first_name} {player.last_name}.")
    
#     # Redirect back to the player's profile page
#     return redirect('show_player', pk=player.pk)



# def respond_invite(request, invite_id):
#     """
#     Allows a player to accept or reject an invitation.
#     """
#     # Get the invitation by its ID, ensuring it belongs to the logged-in player
#     invitation = get_object_or_404(Invitation, id=invite_id, invitee=request.user.player)

#     if request.method == 'POST':
#         # Get the player's response (Accepted or Rejected)
#         response = request.POST.get('response')
#         if response in ['Accepted', 'Rejected']:
#             # Update the invitation status
#             invitation.status = response
#             invitation.save()

#             if response == 'Accepted':
#                 # Get the player's current team, if any
#                 current_team_record = PlaysIn.objects.filter(player=invitation.invitee, end_date__isnull=True).first()

#                 # End the current team's record if it exists
#                 if current_team_record:
#                     current_team_record.end_date = datetime.now()
#                     current_team_record.save()

#                 # Add the player to the new team
#                 PlaysIn.objects.create(
#                     player=invitation.invitee,
#                     team=invitation.inviter.get_team(),
#                     start_date=datetime.now()
#                 )

#             messages.success(request, f"You have {response.lower()} the invitation.")
#         else:
#             messages.error(request, "Invalid response.")
    
#     # Redirect back to the player's inbox
#     return redirect('inbox')


class SendInvitationView(LoginRequiredMixin, View):
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
