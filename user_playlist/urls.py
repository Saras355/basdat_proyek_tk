from django.urls import path
from django.contrib import admin
from user_playlist.views import show_user_playlist, add_user_playlist, delete_playlist, edit_playlist, detail_user_playlist
from user_playlist.views import add_song

app_name = 'main'

urlpatterns = [
    path('', show_user_playlist, name='home'),  # Map root URL to show_user_playlist view
    path('admin/', admin.site.urls),
    path('show_user_playlist/', show_user_playlist, name='show_user_playlist'),
    path('detail_user_playlist/<uuid:playlist_id>/', detail_user_playlist, name='detail_user_playlist'),
    path('delete_playlist/<uuid:playlist_id>/', delete_playlist, name='delete_playlist'),
    path('edit_playlist/<uuid:playlist_id>/', edit_playlist, name='edit_playlist'),
    path('add_user_playlist/', add_user_playlist, name='add_user_playlist'),
    path('add_song/<uuid:playlist_id>/', add_song, name='add_song'),
]