from django.urls import path
from download.views import show_downloaded_song, show_delete_song
app_name = 'download'

urlpatterns = [
    path('downloaded-song/', show_downloaded_song, name='show_downloaded_song'),
    path('downloaded-song/delete/<uuid:song_id>/', show_delete_song, name='show_delete_song')
]
