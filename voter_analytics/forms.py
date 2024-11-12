from django import forms
from .models import *

class SearchVotersForm(forms.Form):
    PARTY_CHOICES = [
        ('', 'Any'),
        ('D', 'Democratic'),
        ('R', 'Republican'),
        ('CC', 'Constitution Party'),
        ('L', 'Libertarian Party'),
        ('T', 'Tea Party'),
        ('O', 'Other'),
        ('G', 'Green Party'),
        ('J', 'Independent Party'),
        ('Q', 'Reform Party'),
        ('FF', 'Freedom Party'),
    ]

    party_affiliation = forms.ChoiceField(
        choices=PARTY_CHOICES,
        required=False,
        label='Party Affiliation'
    )

    min_date_of_birth = forms.ChoiceField(
        choices=[('', 'Select Year')] + [(year, year) for year in range(1900, 2025)],
        required=False,
        label='Born After'
    )
    
    max_date_of_birth = forms.ChoiceField(
        choices=[('', 'Select Year')] + [(year, year) for year in range(1900, 2025)],
        required=False,
        label='Born Before'
    )

    voter_score = forms.ChoiceField(
        choices=[('', 'Any')] + [(i, str(i)) for i in range(6)],
        required=False,
        label='Voter Score'
    )


    # Whether they voted in specific elections (check boxes)
    voted_v20state = forms.BooleanField(required=False, label='2020 State Election')
    voted_v21town = forms.BooleanField(required=False, label='2021 Town Election')
    voted_v21primary = forms.BooleanField(required=False, label='2021 Primary Election')
    voted_v22general = forms.BooleanField(required=False, label='2022 General Election')
    voted_v23town = forms.BooleanField(required=False, label='2023 Town Election')