from django.shortcuts import render

# def init_paket():
    
def show_langganan_paket(request):
    paket = {
        "1 Bulan": 20_000,
        "3 Bulan": 50_000,
        "6 Bulan": 100_000,
        "1 Tahun": 150_000
    }

    context = {
        'paket': paket
    }

    return render(request, "langganan_paket/langganan_paket.html", context)

def show_finalisasi_paket(request, jenis, harga):
    context = {
        'jenis_paket': jenis,
        'harga_paket': harga
    }
    return render(request, "langganan_paket/finalisasi_langganan.html", context)

def show_riwayat_langganan(request):
    riwayat_transaksi = [
        ["1 Bulan", "8 April 2024, 23:00", "8 Mei 2024, 23:00", "E-Wallet", 20_000]
        ]

    context = {
        'riwayat_transaksi': riwayat_transaksi
    }

    return render(request, "langganan_paket/riwayat_langganan.html", context)

def show_hasil_cari(request, query):
    daftar_lagu = [
        ["SONG", "Love is in the air", "Henry Soedibjo"],
        ["SONG", "What is love", "Narendra"],
        ["PODCAST", "Love is Blind Pod", "Johan"],
        ["USER PLAYLIST", "90s Love Songs", "Nano"]
    ]

    context = {
        'query': query,
        'daftar_lagu': daftar_lagu
    }
    return render(request, "search_content/hasil_cari.html", context)

def show_downloaded_song(request):
    daftar_lagu = {
        "artis1": "song1",
        "artis2": "song2",
        "artis3": "song3",
        "artis4": "song4"
    }

    context = {
        'daftar_lagu': daftar_lagu
    }
    return render(request, "downloaded_song/downloaded_song.html", context)

def show_delete_song(request, judul):
    context = {
        'judul': judul
    }
    return render(request, "downloaded_song/delete_song.html", context)