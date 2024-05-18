from django.urls import path
from search.views import show_cari_konten, show_hasil_cari

app_name = 'search'

urlpatterns = [
    path('', show_cari_konten, name='show_cari_konten'),
    path('<str:judul>/', show_hasil_cari, name='show_hasil_cari'),
]