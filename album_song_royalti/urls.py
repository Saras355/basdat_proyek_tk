from django.urls import path
from album_song_royalti.views import *

urlpatterns = [
    #cek royalti
    path('cek-royalti/', cek_royalti, name='cek_royalti'),
    #baru
    path('list-album/', list_album, name='list_album'),
    path('list-album-artist/', list_album_artist, name='list_album_artist'),
    path('daftar-lagu/<uuid:album_id>/', daftar_lagu, name='lihat_daftar_lagu_label'),
    path('daftar-lagu-artist/<uuid:album_id>/', daftar_lagu, name='lihat_daftar_lagu_artist'),
    path('create-album/', create_album, name='create_album'),
    path('create-lagu/<uuid:album_id>/', create_lagu, name='create_lagu'),
    path('hapus-album/<uuid:album_id>/', hapus_album, name='hapus_album'),
    path('hapus-lagu/<uuid:song_id>/', hapus_lagu, name='hapus_lagu'),
    path('index/', index, name='index'),
    path('submit', submit, name='submit'),

    path('entry_album_song_create_list/', entry_album_song_create_list, name='entry_album_song_create_list'),
    path('lihat_detail_lagu/<uuid:song_id>/', lihat_detail_lagu, name='lihat_detail_lagu'),
]
