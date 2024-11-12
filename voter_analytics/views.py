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
            # Apply filters based on form input
            if self.form.cleaned_data['party_affiliation']:
                qs = qs.filter(party_affiliation=self.form.cleaned_data['party_affiliation'])

            if self.form.cleaned_data['min_date_of_birth']:
                qs = qs.filter(date_of_birth__year__gte=self.form.cleaned_data['min_date_of_birth'])
        
            if self.form.cleaned_data['max_date_of_birth']:
                qs = qs.filter(date_of_birth__year__lt=self.form.cleaned_data['max_date_of_birth'])

            if self.form.cleaned_data['voter_score']:
                qs = qs.filter(voter_score=self.form.cleaned_data['voter_score'])

            if self.form.cleaned_data['voted_v20state']:
                qs = qs.filter(v20state=True)

            if self.form.cleaned_data['voted_v21town']:
                qs = qs.filter(v21town=True)

            if self.form.cleaned_data['voted_v21primary']:
                qs = qs.filter(v21primary=True)

            if self.form.cleaned_data['voted_v22general']:
                qs = qs.filter(v22general=True)

            if self.form.cleaned_data['voted_v23town']:
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