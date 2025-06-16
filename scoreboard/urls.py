"""
URL patterns for the scoreboard app.
"""

from django.urls import path
from . import views

app_name = 'scoreboard'

urlpatterns = [
    path('', views.scoreboard, name='scoreboard'),
    path('api/data/', views.scoreboard_data, name='scoreboard_data'),
]
