"""
URL patterns for the core app.
"""

from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('izanami-status/', views.izanami_status, name='izanami_status'),
    path('collect-fragment/<int:fragment_id>/', views.collect_fragment, name='collect_fragment'),
    path('recognize-pattern/', views.recognize_pattern, name='recognize_pattern'),
    path('escape-reality/', views.escape_reality, name='escape_reality'),
    path('accept-reality/', views.accept_reality, name='accept_reality'),
    path('distorted-challenge/<int:challenge_id>/', views.distorted_challenge, name='distorted_challenge'),
    path('loop-analytics/', views.loop_analytics, name='loop_analytics'),
]
