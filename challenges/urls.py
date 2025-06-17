"""
URL patterns for the challenges app.
"""

from django.urls import path
from . import views

app_name = 'challenges'

urlpatterns = [
    path('', views.index, name='index'),
    path('academy/', views.academy_challenges, name='academy'),
    path('chunin/', views.chunin_challenges, name='chunin'),
    path('jonin/', views.jonin_challenges, name='jonin'),
    path('uchiha/', views.uchiha_challenges, name='uchiha'),
    path('<int:challenge_id>/', views.challenge_detail, name='detail'),
    path('<int:challenge_id>/submit/', views.submit_flag, name='submit_flag'),
    path('<int:challenge_id>/hint/', views.unlock_hint, name='unlock_hint'),
    
    # Pygame challenge URLs
    path('pygame/<int:challenge_id>/', views.pygame_challenge, name='pygame_challenge'),
    path('pygame/<int:challenge_id>/game/', views.pygame_game, name='pygame_game'),
    
    # API endpoints for challenges
    path('api/login_check/', views.login_check_api, name='login_check_api'),
    path('api/update_profile/', views.update_profile_api, name='update_profile_api'),
    path('api/get_profile/', views.get_profile_api, name='get_profile_api'),
    
    # Vulnerable endpoints for specific challenges
    path('api/user_data/', views.user_data_api, name='user_data_api'),
    path('api/search/', views.search_api, name='search_api'),
    path('api/file_upload/', views.file_upload, name='file_upload'),
    path('api/fetch_url/', views.fetch_url, name='fetch_url'),
    path('api/execute_command/', views.execute_command, name='execute_command'),
    path('api/deserialize/', views.deserialize_data, name='deserialize_data'),
]
