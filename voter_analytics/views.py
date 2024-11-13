from typing import Any
from django.shortcuts import render, redirect
from django.urls import reverse

from . models import *
from .forms import *
from django.views.generic import *
from django.db.models.functions import *
from django.db.models import *
from django.shortcuts import redirect
import plotly
import plotly.graph_objects as go
import plotly.express as px

# Create your views here.
class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100  # Show 100 records per page

    def get_queryset(self):
        '''Return the filtered set of Voter records.'''

        # Start with the base queryset
        qs = super().get_queryset()

        # Instantiate the form with GET parameters
        self.form = SearchVotersForm(self.request.GET)

        if self.form.is_valid():
            
            # Filtering logic based on GET parameters
            party_affiliation = self.request.GET.get('party_affiliation')
            min_date_of_birth = self.request.GET.get('min_date_of_birth')
            max_date_of_birth = self.request.GET.get('max_date_of_birth')
            voter_score = self.request.GET.get('voter_score')
            voted_v20state = self.request.GET.get('voted_v20state')
            voted_v21town = self.request.GET.get('voted_v21town')
            voted_v21primary = self.request.GET.get('voted_v21primary')
            voted_v22general = self.request.GET.get('voted_v22general')
            voted_v23town = self.request.GET.get('voted_v23town')

            # Apply filters based on form input
            if party_affiliation:
                qs = qs.filter(party_affiliation=party_affiliation)

            if min_date_of_birth:
                qs = qs.filter(date_of_birth__year__gte=min_date_of_birth)

            if max_date_of_birth:
                qs = qs.filter(date_of_birth__year__lte=max_date_of_birth)

            if voter_score:
                qs = qs.filter(voter_score=voter_score)

            if voted_v20state:
                qs = qs.filter(v20state=True)

            if voted_v21town:
                qs = qs.filter(v21town=True)

            if voted_v21primary:
                qs = qs.filter(v21primary=True)

            if voted_v22general:
                qs = qs.filter(v22general=True)

            if voted_v23town:
                qs = qs.filter(v23town=True)

        return qs


    def get_context_data(self, **kwargs):
        '''Add the form to the context.'''
        context = super().get_context_data(**kwargs)

        # Add the form to the context
        context['form'] = self.form  
        return context

class ShowVoterPageView(DetailView):
    '''View to display a single Voter record.'''
    model = Voter
    template_name = 'voter_analytics/show_voter.html'
    context_object_name = 'voter'


class VoterGraphsView(ListView):
    '''View to display a graphs'''
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_queryset(self):
        '''Return the filtered set of Voter records.'''

        # Start with the base queryset
        qs = super().get_queryset()

        # Instantiate the form with GET parameters
        self.form = SearchVotersForm(self.request.GET)

        if self.form.is_valid():
            
            # Filtering logic based on GET parameters
            party_affiliation = self.request.GET.get('party_affiliation')
            min_date_of_birth = self.request.GET.get('min_date_of_birth')
            max_date_of_birth = self.request.GET.get('max_date_of_birth')
            voter_score = self.request.GET.get('voter_score')
            voted_v20state = self.request.GET.get('voted_v20state')
            voted_v21town = self.request.GET.get('voted_v21town')
            voted_v21primary = self.request.GET.get('voted_v21primary')
            voted_v22general = self.request.GET.get('voted_v22general')
            voted_v23town = self.request.GET.get('voted_v23town')

            # Apply filters based on form input
            if party_affiliation:
                qs = qs.filter(party_affiliation=party_affiliation)

            if min_date_of_birth:
                qs = qs.filter(date_of_birth__year__gte=min_date_of_birth)

            if max_date_of_birth:
                qs = qs.filter(date_of_birth__year__lte=max_date_of_birth)

            if voter_score:
                qs = qs.filter(voter_score=voter_score)

            if voted_v20state:
                qs = qs.filter(v20state=True)

            if voted_v21town:
                qs = qs.filter(v21town=True)

            if voted_v21primary:
                qs = qs.filter(v21primary=True)

            if voted_v22general:
                qs = qs.filter(v22general=True)

            if voted_v23town:
                qs = qs.filter(v23town=True)

        return qs

    def get_context_data(self, **kwargs):
        '''Add the form to the context.'''
        context = super().get_context_data(**kwargs)

        # Add the form to the context
        context['form'] = self.form 

        # filtered queryset to get filtered data
        # filtered_qs = self.get_queryset()


        # # Query to get voter count by birth year
        # birth_year_counts = (
        #     filtered_qs
        #     .annotate(birth_year=ExtractYear('date_of_birth'))
        #     .values('birth_year')
        #     .annotate(count=Count('birth_year'))
        #     .order_by('birth_year')
        # )

        # # Prepare x and y 
        # x_birth_years = [entry['birth_year'] for entry in birth_year_counts]
        # y_birth_counts = [entry['count'] for entry in birth_year_counts]

        # # Voter Birth Year Distribution graph
        # birth_year_histogram = px.bar(
        #     x=x_birth_years,
        #     y=y_birth_counts,
        #     title='Voter Birth Year Distribution',
        #     labels={'x': 'Birth Year', 'y': 'Number of Voters'}
        # )

        # # Convert figure to HTML and add it to the context
        # context['birth_year_chart'] = birth_year_histogram.to_html(full_html=False)


        # # Query to get voter count by party affiliation
        # party_counts = (
        #     filtered_qs
        #     .values('party_affiliation')
        #     .annotate(count=Count('party_affiliation'))
        #     .order_by('-count')
        # )

        # labels = [entry['party_affiliation'] for entry in party_counts]
        # values = [entry['count'] for entry in party_counts]

        # # Voter Party Affiliation Pie Chart
        # party_pie_chart = px.pie(
        #     names=labels,
        #     values=values,
        #     title='Voter Distribution by Party',
        #     labels={'names': 'Party Affiliation', 'values': 'Number of Voters'}
        # )
        # context['party_pie_chart'] = party_pie_chart.to_html(full_html=False)


        # voter_counts = (
        #     self.get_queryset()
        #     .values('voter_score')
        #     .annotate(count=Count('voter_score'))
        #     .order_by('voter_score')
        # )

        # # Field names and voter counts
        # election_fields_with_counts = {
        #     '2020 State Election': filtered_qs.filter(v20state=True).count(),
        #     '2021 Town Election': filtered_qs.filter(v21town=True).count(),
        #     '2021 Primary Election': filtered_qs.filter(v21primary=True).count(),
        #     '2022 General Election': filtered_qs.filter(v22general=True).count(),
        #     '2023 Town Election': filtered_qs.filter(v23town=True).count(),
        # }

        # x_elections = list(election_fields_with_counts.keys())  # Labels
        # y_vote_counts = list(election_fields_with_counts.values())  # Counts

        # # Vote Count by Election
        # election_bar_chart = px.bar(
        #     x=x_elections,
        #     y=y_vote_counts,
        #     title=f'Vote Count by Election (n={filtered_qs.count()})',
        #     labels={'x': 'Election', 'y': 'Number of Voters'}
        # )

        # context['election_chart'] = election_bar_chart.to_html(full_html=False)

        
        return context 