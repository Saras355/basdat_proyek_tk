from django.urls import path
from main.views import show_finalisasi_paket, show_hasil_cari, show_langganan_paket,show_riwayat_langganan
from main.views import show_downloaded_song, show_delete_song, show_cari_konten
app_name = 'main'

urlpatterns = [
    path('langganan/', show_langganan_paket, name='show_langganan_paket'),
    path('langganan/<str:jenis>/<int:harga>/', show_finalisasi_paket, name='show_finalisasi_paket'),
    path('langganan/riwayat-langganan/', show_riwayat_langganan, name='show_riwayat_langganan'),
    path('search/', show_cari_konten, name='show_cari_konten'),
    path('search/<str:judul>/', show_hasil_cari, name='show_hasil_cari'),
    path('downloaded-song/', show_downloaded_song, name='show_downloaded_song'),
    path('downloaded-song/delete/<str:judul>/', show_delete_song, name='show_delete_song')
]