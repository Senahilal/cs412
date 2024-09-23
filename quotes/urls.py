##quotes/urls.py

from django.urls import path
from django.conf import settings
from . import views

urlpatterns =[
    path(r'', views.main_page, name="main"),  #main
    path('quote/', views.quote, name="quote"),  #quote
    path('show_all/', views.show_all, name="show_all"),  #show_all
    path('about/', views.about, name="about"),  #about

]