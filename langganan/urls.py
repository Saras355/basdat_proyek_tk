from django.urls import path
from langganan.views import show_finalisasi_paket, show_langganan_paket, show_riwayat_langganan, beli_paket
app_name = 'langganan'

urlpatterns = [
    path('', show_langganan_paket, name='show_langganan_paket'),
    path('<str:jenis>/<int:harga>/', show_finalisasi_paket, name='show_finalisasi_paket'),
    path('riwayat-langganan/', show_riwayat_langganan, name='show_riwayat_langganan'),
    path('beli_paket/', beli_paket, name='beli_paket')
]