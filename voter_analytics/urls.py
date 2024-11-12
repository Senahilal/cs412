#voter_analytics/urls.py

from django.urls import path
from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views

urlpatterns =[
    path('', views.VoterListView.as_view(), name='voters'),
    path('voter/<int:pk>/', views.ShowVoterPageView.as_view(), name='voter_page'),
    path('graphs/', views.VoterGraphsView.as_view(), name='graphs'),
]