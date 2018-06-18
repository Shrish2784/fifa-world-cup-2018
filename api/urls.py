from django.urls import path
from . import views


urlpatterns = [
    path('matches/', views.index, name='index'),
    path('sync/current_match/', views.sync_current_match, name='sync_current_match'),
    path('sync/matches/', views.sync_matches, name='sync_matches'),
    path('test/past/', views.past_match_response, name='test_past'),
    path('test/current/', views.current_match_response, name='test_current'),
    path('test/future/', views.future_match_response, name='test_future'),
    path('test/empty/', views.empty_response, name='test_empty')
]
