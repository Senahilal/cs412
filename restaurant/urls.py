##restaurant/urls.py

from django.urls import path
from django.conf import settings
from . import views

urlpatterns =[
    path('main/', views.main, name="main"),  #main - information about the restaurant
    path('order/', views.order , name="order"),  #order - display an online order form
    path('confirmation/', views.confirmation, name="confirmation"),  #confirmation - a confirmation page to display after the order is placed
]