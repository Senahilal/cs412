from typing import Any
from django.shortcuts import render, redirect
from django.urls import reverse

from . models import *
from .forms import *
from django.views.generic import *
from django.shortcuts import redirect

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

        
        return context 