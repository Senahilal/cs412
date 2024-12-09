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
        '''Return a string representation of this Player.'''
        return f"{self.first_name} {self.last_name}"
    
    def get_absolute_url(self):
        '''Return a URL to show this one profile'''
        return reverse('show_player', kwargs={'pk': self.pk})
    
    def get_current_team(self):
        ''' Returns the current team of the player, if any.'''
        current_team_record = PlaysIn.objects.filter(player=self, end_date__isnull=True).first()
        return current_team_record.team if current_team_record else None

    def get_old_teams(self):
        '''Returns a queryset of teams the player was previously part of.'''
        return Team.objects.filter(playsin__player=self, playsin__end_date__isnull=False)
    
    def respond_to_invitation(self, invitation, response):
        '''
        Responds to the given invitation with 'Accepted' or 'Rejected'.
        '''
        if invitation.invitee != self:
            raise ValueError("This invitation does not belong to the current player.")

        if response not in ['Accepted', 'Rejected']:
            raise ValueError("Invalid response. Must be 'Accepted' or 'Rejected'.")

        # Update the invitation status
        invitation.status = response
        invitation.save()

        if response == 'Accepted':
            # Update the end date for the player's current team
            current_team_record = PlaysIn.objects.filter(player=self, end_date__isnull=True).first()
            if current_team_record:
                current_team_record.end_date = datetime.now()
                current_team_record.save()

            # Add the player to the manager's team
            PlaysIn.objects.create(
                player=self,
                team=invitation.inviter.get_team(),
                start_date=datetime.now()
            )

        return f"Invitation {response.lower()} successfully."

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
        '''Return a string representation of this Manager.'''
        return f"{self.first_name} {self.last_name}"
    
    def get_absolute_url(self):
        '''Return a URL to show this one profile'''
        return reverse('show_manager', kwargs={'pk': self.pk})
    
    def get_team(self):
        '''Returns the team managed by this manager.'''
        return Team.objects.filter(manager=self).first()
    
    def get_players_in_team(self):
        '''Returns all players in the team managed by this manager.'''
        team = self.get_team()
        if team:
            return team.get_current_players()
        return []
    
    def get_pending_invitees(self):
        '''
        Returns a queryset of players who have pending invitations from this manager.
        '''
        return Player.objects.filter(receiver__inviter=self, receiver__status="Pending")
    
    def send_invitation(self, player):
        '''
        Sends an invitation to the specified player if conditions are met.
        '''
        # Check if the player is already in the manager's team
        if player in self.get_players_in_team():
            raise ValueError("Player is already in your team.")

        # Check for an existing pending invitation
        existing_invitation = Invitation.objects.filter(inviter=self, invitee=player, status='Pending').first()
        if existing_invitation:
            raise ValueError("An invitation is already pending for this player.")

        # Create the invitation
        Invitation.objects.create(inviter=self, invitee=player)
        return "Invitation sent successfully."

    def respond_to_match_request(self, match_request, response):
        ''' Responds to the given match request with 'Accepted' or 'Rejected'.'''

        #
        if match_request.receiver != self:
            raise ValueError("This match request does not belong to the current manager.")

        # Update the match request status
        match_request.status = response
        match_request.save()

        if response == 'Accepted':
            # Create and add the match to the database
            Match.objects.create(
                home_team=match_request.sender.get_team(),
                away_team=self.get_team(),
                date=match_request.date
            )

        return f"Match request {response.lower()} successfully."


class Team(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)

    def __str__(self):
        '''Return a string representation of this Team.'''
        return self.name
    
    def get_current_players(self):
        '''Returns all players currently in this team.'''
        return Player.objects.filter(playsin__team=self, playsin__end_date__isnull=True)

    def get_old_players(self):
        ''' Returns all players who were previously part of this team. '''
        return Player.objects.filter(playsin__team=self, playsin__end_date__isnull=False)
    
    def get_matches(self):
        ''' Returns all matches for this team, ordered by date.'''
        return Match.objects.filter(models.Q(home_team=self) | models.Q(away_team=self)).order_by('date')
    
    def get_played_matches(self):
        ''' Returns all played matches for this team (before the current time and date) '''
        return self.get_matches().filter(date__lte=datetime.now().date()).order_by('-date')
    
    def get_future_matches(self):
        '''
        Returns all future matches for this team.
        '''
        return self.get_matches().filter(date__gte=datetime.now().date()).order_by('date')
    
    def get_standings_data(self):
        '''Returns statistics for the team.
        This method calculates various statistics:
        - Games played
        - Wins
        - Losses
        - Draws
        - Sets won
        - Points (3*win) +1 ==> every win 3 points and every draw 1 point
        '''

        # all of matches this team played and scheduled 
        matches = Match.objects.filter(
            models.Q(home_team=self) | models.Q(away_team=self)
        )

        # The matches this team played
        # when home or away team any of the score must not be null
        games_played = matches.filter(home_score__isnull=False).count()

        #Total number of matches this team won
        wins = matches.filter(
            models.Q(home_team=self, home_score__gt=models.F('away_score')) |
            models.Q(away_team=self, away_score__gt=models.F('home_score'))
        ).count()

        #Total number of matches this team lost
        losses = matches.filter(
            models.Q(home_team=self, home_score__lt=models.F('away_score')) |
            models.Q(away_team=self, away_score__lt=models.F('home_score'))
        ).count()

        #Draws
        draws = matches.filter(
            models.Q(home_team=self, home_score=models.F('away_score')) |
            models.Q(away_team=self, away_score=models.F('home_score'))
        ).count()

        #if this team played game 
        if games_played > 0:
            sets_won =0

            #Total number of goals scored by this team
            # = total number of sets this team won
            sets_won = matches.filter(home_team=self).aggregate(total=models.Sum('home_score'))['total'] or 0
            sets_won += matches.filter(away_team=self).aggregate(total=models.Sum('away_score'))['total'] or 0


        #Calculating points based on wins and draws
        points = (wins * 3) + draws

        #dictionary containing the team's standings data
        return {
            "games_played": games_played,
            "wins": wins,
            "losses": losses,
            "draws": draws,
            "points": points,
            "sets_won": sets_won,
        }

class Match(models.Model):
    date = models.DateField()
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_team')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_team')
    home_score = models.IntegerField(blank=True, null=True)
    away_score = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.home_team} vs {self.away_team} on {self.date}"
    
    def get_all_played_matches():
        '''Returns all matches that have been played.'''
        # date__lte=datetime.now().date()
        return Match.objects.filter(date__lte=datetime.now().date()).order_by('-date')
    
    def get_all_scheduled_matches():
        '''Returns all matches that are scheduled for the future.'''
        return Match.objects.filter(date__gte=datetime.now().date()).order_by('date')

class PlaysIn(models.Model):
    '''Represents a relation between a team and a player.'''
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True) #null when player is currently in the team

    def __str__(self):
        '''Return a string representation of this model.'''
        #If player is not playing in this team anymore
        if self.end_date:
            return f"{self.player} played in {self.team} from {self.start_date} to {self.end_date}"
        else:
            return f"{self.player} plays in {self.team}" #player is currently playing in this team


class Invitation(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    inviter = models.ForeignKey('Manager', on_delete=models.CASCADE, related_name='sender')
    invitee = models.ForeignKey('Player', on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    timestamp = models.DateTimeField(default=datetime.now)

    def __str__(self):
        '''Return a string representation of this Invitation.'''
        return f"Invitation from {self.inviter} to {self.invitee} - {self.status}"

class MatchRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    sender = models.ForeignKey('Manager', on_delete=models.CASCADE, related_name='match_sender')
    receiver = models.ForeignKey('Manager', on_delete=models.CASCADE, related_name='match_receiver')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    timestamp = models.DateTimeField(default=datetime.now)

    def __str__(self):
        '''Return a string representation of this MatchRequest.'''
        return f"Match request from {self.sender} to {self.receiver} - {self.timestamp}"