from django.urls import path
from play_podcast.views import *

app_name = 'podcast'

urlpatterns = [    
    path('chart-detail/<str:playlist_id>/', show_chart_detail, name='show_chart_detail'),
    path('chart-list', show_chart_list, name='show_chart_list'),
    path('delete-podcast/<str:podcast_id>/', delete_podcast, name='delete_podcast'),
    path('<str:podcast_id>/', show_detail_podcast, name='show_detail_podcast'),
    path('', manage_podcasts, name='manage_podcasts'),
]