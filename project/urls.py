#project/urls.py

from django.urls import path
from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views

urlpatterns =[
    path('', views.ShowAllMatchesView.as_view(), name="show_all_matches"),
    path('matches', views.ShowAllMatchesView.as_view(), name="show_all_matches"),
    path('teams', views.ShowAllTeamsView.as_view(), name="show_all_teams"),
    path('team/<int:pk>/', views.ShowTeamPageView.as_view(), name="show_team"),
    path('create_player/',views.CreatePlayerView.as_view(), name='create_player'),
    path('create_manager/',views.CreateManagerView.as_view(), name='create_manager'),
    path('player/<int:pk>/', views.ShowPlayerPageView.as_view(), name='show_player'),
    path('manager/<int:pk>/', views.ShowManagerPageView.as_view(), name='show_manager'),
    path('inbox/', views.InboxView.as_view(), name='inbox'),
    # path('send_invite/<int:player_id>/', views.send_invite, name='send_invite'),
    # path('respond_invite/<int:invite_id>/', views.respond_invite, name='respond_invite'),
    path('player/send_invite/<int:player_pk>/', views.SendInvitationView.as_view(), name='send_invite'),
    path('invitation/respond/<int:invite_pk>/', views.RespondInvitationView.as_view(), name='respond_invite'),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='project_login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='show_all_matches'), name='project_logout'),
    ]