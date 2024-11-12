from typing import Any
from django.shortcuts import render, redirect
from django.urls import reverse

from . models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.shortcuts import redirect

# Create your views here.
class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100  # Show 100 records per page