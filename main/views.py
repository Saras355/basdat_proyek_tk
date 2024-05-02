from django.shortcuts import render, redirect

def show_navbar(request):
    context = {

    }
    return render(request, "navbar.html", context)
    
def show_langganan_paket(request):
    paket = {
        "1 Bulan": 60_000,
        "3 Bulan": 180_000,
        "6 Bulan": 350_000,
        "1 Tahun": 600_000
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

def show_cari_konten(request):
    if 'query' in request.GET:
        query = request.GET['query']
        return redirect(f'/search/{query}')
    
    return render(request, "search_content/cari_konten.html")

def show_hasil_cari(request, judul):
    daftar_lagu = [
        ["SONG", "Love is in the air", "John Doe"],
        ["SONG", "What is love", "Ada"],
        ["PODCAST", "Love is Blind Pod", "Laplace"],
        ["USER PLAYLIST", "90s Love Songs", "Kleene"]
    ]

    if 'query' in request.GET:
        judul = request.GET['query']

    flag = any(judul.lower() in lagu[1].lower() for lagu in daftar_lagu)

    context = {
        'judul': judul,
        'daftar_lagu': daftar_lagu
    }

    if flag is True:
        return render(request, "search_content/hasil_cari.html", context)
    else:
        return render(request, "search_content/hasil_cari_not_found.html", context)

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