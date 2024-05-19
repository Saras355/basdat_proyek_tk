from datetime import timedelta
from pyexpat.errors import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
import psycopg2
from django.db import connection

def show_navbar(request):
    return render(request, "navbar.html")

def list_tables(request):
    query = """
    select nama
    from marmut.akun
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
        for res in result:
            print(res[0])
        
    return render(request, 'tes.html')
    
def show_langganan_paket(request):
    user_data = request.session.get('user_data', {})

    query = """
    set search_path to marmut;
    select * from paket
    """
    
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

    print("\n================ DEBUG AREA ================")
    for key, value in user_data.items():
        print(f"{key}: {value}")
    print("================ DEBUG AREA ================\n")

    paket = {
        result[0][0]: result[0][1],
        result[1][0]: result[1][1],
        result[2][0]: result[2][1],
        result[3][0]: result[3][1]
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

def beli_paket(request):
    print("INI METHODNYA: " + request.method)
    if request.method == 'POST':
        user_data = request.session.get('user_data', {})
        email = user_data.get('email')
        jenis_paket = request.POST.get('jenis_paket')
        metode_bayar = request.POST.get('metode_bayar')
        harga_paket = int(request.POST.get('harga_paket'))
        timestamp_dimulai = timezone.now()
        if (jenis_paket == "1 bulan"):
            timestamp_berakhir = timestamp_dimulai + timedelta(days=30)
        elif (jenis_paket == "2 bulan"):
            timestamp_berakhir = timestamp_dimulai + timedelta(days=60)
        elif (jenis_paket == "6 bulan"):
            timestamp_berakhir = timestamp_dimulai + timedelta(days=180)
        else:
            timestamp_berakhir = timestamp_dimulai + timedelta(days=365)

        print(email)
        print(jenis_paket)
        print(metode_bayar)
        print(harga_paket)
        print(timestamp_dimulai)
        print(timestamp_berakhir)

        if not email or not jenis_paket or not metode_bayar or not harga_paket:
            return JsonResponse({'error': 'Data tidak lengkap'}, status=400)

        insert_query = """
        SET search_path TO marmut;
        INSERT INTO TRANSACTION (id, jenis_paket, email, timestamp_dimulai, timestamp_berakhir, metode_bayar, nominal)
        VALUES (gen_random_uuid(), %s, %s, %s, %s, %s, %s);
        """

        try:
            with connection.cursor() as cursor:
                cursor.execute(insert_query, [jenis_paket, email, timestamp_dimulai, timestamp_berakhir, metode_bayar, harga_paket])

            # Tambahkan entri di tabel PREMIUM
            insert_premium_query = """
            INSERT INTO PREMIUM (email) VALUES (%s)
            ON CONFLICT (email) DO NOTHING;
            """
            with connection.cursor() as cursor:
                cursor.execute(insert_premium_query, [email])
                cursor.execute("DELETE FROM marmut.nonpremium WHERE email = %s", (email,))
            user_data["is_premium"] = True

            print("\n================ DEBUG AREA ================")
            for key, value in user_data.items():
                print(f"{key}: {value}")
            print("================ DEBUG AREA ================\n")

            return JsonResponse({'success': 'Paket langganan berhasil dibeli'}, status=200)
        
        except (Exception, psycopg2.DatabaseError) as error:
            print("\n================ DEBUG AREA ================")
            for key, value in user_data.items():
                print(f"{key}: {value}")
            print("================ DEBUG AREA ================\n")
            return JsonResponse({'error': str(error)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def show_riwayat_langganan(request):
    user_data = request.session.get('user_data', {})
    email = user_data['email']

    query = """
    SELECT jenis_paket, TO_CHAR(timestamp_dimulai, 'DD Month YYYY, HH24:MI'),
    TO_CHAR(timestamp_berakhir, 'DD Month YYYY, HH24:MI'), metode_bayar, 
    TO_CHAR(nominal, '999,999')
    FROM marmut.transaction
    WHERE email = %s;
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (email,))
        riwayat_transaksi = cursor.fetchall()
        print(riwayat_transaksi)

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
    # judul = str(judul)
    if 'query' in request.GET:
        judul = request.GET['query']
    
    like_pattern = f'%{judul}%'
    flag = True

    song_query = """
    SET search_path to MARMUT;
    SELECT K.judul AS Title, A.nama AS Creator, K.id AS ContentID
    FROM SONG S
    JOIN KONTEN K ON S.id_konten = K.id
    JOIN ARTIST AR ON S.id_artist = AR.id
    JOIN AKUN A ON AR.email_akun = A.email
    WHERE K.judul LIKE %s;
    """

    podcast_query = """
    SET search_path to MARMUT;
    SELECT K.judul AS Title, A.nama AS Creator, K.id AS ContentID
    FROM PODCAST P
    JOIN KONTEN K ON P.id_konten = K.id
    JOIN PODCASTER PC ON P.email_podcaster = PC.email
    JOIN AKUN A ON PC.email = A.email
    WHERE K.judul ILIKE %s;
    """

    playlist_query = """
    SET search_path to MARMUT;
    SELECT UP.judul AS Title, A.nama AS Creator, UP.id_user_playlist AS ContentID
    FROM USER_PLAYLIST UP
    JOIN AKUN A ON UP.email_pembuat = A.email
    WHERE UP.judul LIKE %s;
    """

    with connection.cursor() as cursor:
        cursor.execute(song_query, [like_pattern])
        songs = cursor.fetchall()
        print(songs)

        cursor.execute(podcast_query, [like_pattern])
        podcasts = cursor.fetchall()
        print(podcasts)

        cursor.execute(playlist_query, [like_pattern])
        playlists = cursor.fetchall()
        print(playlists)
    
    if (len(songs) == len(podcasts) == len(playlists) == 0):
        flag = False
    print(flag)

    context = {
        'songs': songs,
        'podcasts': podcasts,
        'playlists': playlists,
        'search_substring': judul,
    }

    if flag is True:
        return render(request, "search_content/hasil_cari.html", context)
    else:
        return render(request, "search_content/hasil_cari_not_found.html", context)

def show_downloaded_song(request):
    user_data = request.session.get('user_data', {})
    email = user_data.get('email')
    print(email)

    query = """
    set search_path to marmut;
    SELECT k.judul, ak.nama, s.id_konten
    FROM downloaded_song ds
    JOIN song s ON ds.id_song = s.id_konten
    JOIN artist a ON s.id_artist = a.id
    JOIN konten k ON s.id_konten = k.id
    JOIN akun ak ON ak.email = a.email_akun
    WHERE ds.email_downloader = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, [email])
        songs = cursor.fetchall()
        print(songs)
        for song in songs:
            print(song[2])
    
    context = {
        'songs': songs
    }
    return render(request, "downloaded_song/downloaded_song.html", context)

def show_delete_song(request, song_id):
    user_data = request.session.get('user_data', {})
    email = user_data.get('email')

    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM marmut.downloaded_song WHERE email_downloader = %s AND id_song = %s", (email, song_id,))
        cursor.execute("SELECT judul FROM marmut.konten WHERE id = %s", (song_id,))
        title = cursor.fetchone()[0]
    
    context = {
        'title': title
    }
    return render(request, "downloaded_song/delete_song.html", context)