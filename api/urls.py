from django.urls import path
from . import views


urlpatterns = [
    path('match/', views.index, name='index'),
    path('sync/currentMatch/', views.sync_current_match, name='sync_currentMatch'),
    path('sync/matches/ ', views.sync_past_future_match, name='sync_matches')
]
