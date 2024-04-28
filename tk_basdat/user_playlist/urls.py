from django.urls import path
# from main.views import show_main, create_user_playlist, show_xml, show_json, show_xml_by_id, show_json_by_id 
# from main.views import user_playlist_detail, edit_user_playlist, delete_user_playlist 
from django.contrib import admin
from user_playlist.views import show_user_playlist, playlist_detail, delete_playlist, edit_playlist, add_playlist


app_name = 'main'

urlpatterns = [
    path('', show_user_playlist, name='home'),  # Map root URL to show_user_playlist view
    path('admin/', admin.site.urls),
    path('show_user_playlist/', show_user_playlist, name='show_user_playlist'),
    path('playlist_detail/<uuid:playlist_id>/', playlist_detail, name='playlist_detail'),
    path('delete_playlist/<uuid:playlist_id>/', delete_playlist, name='delete_playlist'),
    path('edit_playlist/<uuid:playlist_id>/', edit_playlist, name='edit_playlist'),
    path('add_playlist/', add_playlist, name='add_playlist'),
]