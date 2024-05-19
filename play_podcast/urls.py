from django.urls import path
from play_podcast.views import *

app_name = 'play_podcast'

urlpatterns = [    
    path('chart-detail/<str:playlist_id>/', show_chart_detail, name='show_chart_detail'),
    path('chart-list', show_chart_list, name='show_chart_list'),
    path('delete-podcast/<str:podcast_id>/', delete_podcast, name='delete_podcast'),
    path('<str:podcast_id>/', show_detail_podcast, name='show_detail_podcast'),
    path('', manage_podcasts, name='manage_podcasts'),
    path('delete-episode/<str:podcast_id>/<str:episode_id>/', delete_episode, name='delete_episode'),
    path('manage-episodes/<str:podcast_id>/', manage_episodes, name='manage_episodes'),
    path('kelola-podcast',kelola_podcast,name='kelola_podcast')
]