from django.urls import path
from play_podcast.views import *

app_name = 'podcast'

urlpatterns = [
    path('chart-detail/<str:playlist_id>/', show_chart_detail, name='show_chart_detail'),
]