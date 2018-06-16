from django.urls import path
from . import views


urlpatterns = [
    path('matches/', views.index, name='index'),
    path('sync/current_match/', views.sync_current_match, name='sync_current_match'),
    path('sync/matches/', views.matches, name='sync_matches')
]
