from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core import serializers
from user_playlist.forms import AddUserPlaylistForm, EditUserPlaylistForm
from django.urls import reverse
from function.general import query_result
from django.db import connection
import datetime
import uuid
# from user_playlist.models import User_playlist
# from connect_postgres import execute_sql_query, execute_sql_query_no_fetch

def show_user_playlist(request):
    playlists = query_result(f"""
    SELECT * FROM marmut.user_playlist;
    """)
    context = {'playlists':playlists}
    return render(request, "show_user_playlist.html", context)

def add_user_playlist(request):
    if request.method == 'POST':
        judul = request.POST.get('judul')
        deskripsi = request.POST.get('deskripsi')
        id_playlist = str(uuid.uuid4())  # Buat id_playlist baru
        # Simpan id_playlist baru ke dalam tabel "playlist"
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO marmut.playlist (id) VALUES (%s);", [id_playlist])
        
        # Setelah mendapatkan id_playlist, gunakan id_playlist tersebut saat menyimpan data user_playlist
        #if playlist baru
        with connection.cursor() as cursor:
            cursor.execute(""" 
            INSERT INTO marmut.user_playlist (email_pembuat, judul, deskripsi, jumlah_lagu, tanggal_dibuat, id_user_playlist, id_playlist, total_durasi)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """, ["fyang@hotmail.com", judul, deskripsi, 0, datetime.date.today(), str(uuid.uuid4()), id_playlist, 0])
        return redirect('user_playlist:show_user_playlist')
        #elseif lagunya udh ada 

    return render(request, 'add_user_playlist.html')

def delete_playlist(request, playlist_id):
    # Hapus user playlist berdasarkan id_playlist
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM marmut.user_playlist WHERE id_playlist = %s;", [playlist_id])
    
    # Hapus playlist berdasarkan id_playlist
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM marmut.playlist WHERE id = %s;", [playlist_id])
    
    # Redirect ke halaman show_user_playlist setelah berhasil menghapus
    return redirect('user_playlist:show_user_playlist')

def edit_playlist(request, playlist_id):
    playlist = query_result(f"SELECT * FROM marmut.user_playlist WHERE id_playlist = '{playlist_id}';")
    if not playlist:
        return HttpResponse("Playlist not found", status=404)
    playlist = playlist[0]

    if request.method == 'POST':
        form = EditUserPlaylistForm(request.POST)
        if form.is_valid():
            judul = form.cleaned_data['judul']
            deskripsi = form.cleaned_data['deskripsi']
            
            with connection.cursor() as cursor:
                cursor.execute("""
                UPDATE marmut.user_playlist
                SET judul = %s, deskripsi = %s
                WHERE id_playlist = %s;
                """, [judul, deskripsi, playlist_id])
            
            return redirect('user_playlist:show_user_playlist')
    else:
        form = EditUserPlaylistForm(initial={'judul': playlist['judul'], 'deskripsi': playlist['deskripsi']})

    context = {'form': form, 'playlist_id': playlist_id}
    return render(request, 'edit_playlist.html', context)

def detail_user_playlist(request, playlist_id):
    # Fetch playlist details
    playlist = query_result(f"""
    SELECT up.*, a.nama as pembuat
    FROM marmut.user_playlist up
    JOIN marmut.akun a ON up.email_pembuat = a.email
    WHERE up.id_playlist = '{playlist_id}';
    """)

    # Fetch songs in the playlist (this is a placeholder, adjust according to your database schema)
    songs = query_result(f"""
    SELECT k.id, k.judul, k.durasi, k.tanggal_rilis, ak.nama as oleh
    FROM marmut.playlist_song ps
    JOIN marmut.konten k ON k.id = ps.id_song
    JOIN marmut.song s ON s.id_konten = k.id
    JOIN marmut.artist ar ON s.id_artist = ar.id
    JOIN marmut.akun ak ON ak.email = ar.email_akun
    WHERE ps.id_playlist = '{playlist_id}';
    """)

    if not playlist:
        return HttpResponse("Playlist not found", status=404)

    context = {
        'playlist': playlist[0],
        'songs': songs,
    }

    return render(request, 'detail_user_playlist.html', context)

def add_song(request, playlist_id):
    if request.method == 'POST':
        song_id = request.POST.get('song_id')

        # Check if the song is already in the playlist
        # existing_song = query_result(f"""
        #     SELECT s.* FROM marmut.user_playlist up
        #     JOIN marmut.playlist_song ps ON ps.id_playlist = up.id_playlist
        #     JOIN marmut.song s ON ps.id_song = s.id_konten
        #     WHERE up.id_playlist = '{playlist_id}' AND s.id_konten = '{song_id}';
        # """)
        # if existing_song:
        #     return HttpResponse("Lagu sudah ada di dalam playlist", status=400)

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO marmut.playlist_song (id_playlist, id_song) VALUES (%s, %s);", 
                           [playlist_id, song_id])

        return redirect(reverse('user_playlist:detail_user_playlist', args=[playlist_id]))

    # Get the list of all songs for the dropdown
    songs = query_result(f"""
        SELECT s.id_konten, k.judul, a.nama as artist
        FROM marmut.song s
        JOIN marmut.konten k ON s.id_konten = k.id 
        JOIN marmut.artist ar ON s.id_artist = ar.id
        JOIN marmut.akun a ON ar.email_akun = a.email;
    """)

    return render(request, 'add_song.html', {'songs': songs, 'playlist_id': playlist_id})

def delete_song(request, playlist_id, song_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM marmut.playlist_song WHERE id_playlist = %s AND id_song = %s;", 
                        [playlist_id, song_id])

    return redirect(reverse('user_playlist:detail_user_playlist', args=[playlist_id]))

def play_song(request, playlist_id, song_id):
    playlist = query_result(f"""
    SELECT up.*, a.nama as pembuat
    FROM marmut.user_playlist up
    JOIN marmut.akun a ON up.email_pembuat = a.email
    WHERE up.id_playlist = '{playlist_id}';
    """)

    song_details = query_result(f"""
        SELECT k.judul, g.genre, ak_artist.nama as artist, ak_songwriter.nama as songwriter, k.durasi, k.tanggal_rilis, k.tahun, s.total_play, s.total_download, al.judul as album, s.id_konten
        FROM marmut.playlist_song ps
        JOIN marmut.song s ON ps.id_song = s.id_konten
        JOIN marmut.konten k ON s.id_konten = k.id
        JOIN marmut.artist ar ON s.id_artist = ar.id
        JOIN marmut.akun ak_artist ON ar.email_akun = ak_artist.email
        JOIN marmut.album al ON s.id_album = al.id
        JOIN marmut.genre g ON s.id_konten = g.id_konten
        JOIN marmut.songwriter_write_song sws ON s.id_konten = sws.id_song
        JOIN marmut.songwriter sw ON sws.id_songwriter = sw.id
        JOIN marmut.akun ak_songwriter ON sw.email_akun = ak_songwriter.email
        WHERE ps.id_playlist = '{playlist_id}' AND ps.id_song = '{song_id}';
    """)

    if not song_details:
        return HttpResponse("Song not found", status=404)

    # Check if user has a premium account
    # user_email = request.user.email  # Assuming you have user authentication and can get the user's email
    # user_info = query_result(f"SELECT is_premium FROM marmut.akun WHERE email = '{user_email}';")
    # is_premium = user_info[0]['is_premium'] if user_info else False

    context = {
        'song': song_details[0],
        # 'is_premium': is_premium
        'playlist': playlist[0]
    }

    return render(request, 'play_song.html', context)

def add_song_to_another_playlist(request, playlist_id, song_id):
    success_message = None
    playlist_name = None
    song_title = None
    
    if request.method == 'POST':
        other_playlist_id = request.POST.get('other_playlist_id')
        with connection.cursor() as cursor:
            # Fetch song title
            song_title_query = query_result("SELECT judul FROM marmut.konten WHERE id = %s", [song_id])
            if song_title_query:
                song_title = song_title_query[0]['judul']

            # Fetch playlist name
            playlist_name_query = query_result("SELECT judul FROM marmut.user_playlist WHERE id_playlist = %s", [other_playlist_id])
            if playlist_name_query:
                playlist_name = playlist_name_query[0]['judul']
            
            cursor.execute("INSERT INTO marmut.playlist_song (id_playlist, id_song) VALUES (%s, %s);", 
                           [other_playlist_id, song_id])
        
            success_message = f"Berhasil menambahkan Lagu dengan judul '{song_title}' ke '{playlist_name}'!"
        return redirect(reverse('user_playlist:detail_user_playlist', args=[playlist_id]))

    # Fetch playlists created by the current user
    playlists = query_result(f"""
        SELECT id_playlist, judul FROM marmut.user_playlist WHERE email_pembuat = %s;
    """, ["fyang@hotmail.com"])

    # Fetch song details
    song = query_result(f"""
        SELECT k.judul, a.nama as artist
        FROM marmut.song s
        JOIN marmut.konten k ON s.id_konten = k.id 
        JOIN marmut.artist ar ON s.id_artist = ar.id
        JOIN marmut.akun a ON ar.email_akun = a.email
        WHERE s.id_konten = %s;
    """, [song_id])
    song = song[0] if song else None

    context = {
        'playlists': playlists,
        'playlist_id': playlist_id,
        'song_id': song_id,
        'song': song,
        'success_message': success_message,
        'playlist_name': playlist_name
    }

    return render(request, 'add_song_to_another_playlist.html', context)

def download_song(request, playlist_id, song_id):
    email_downloader = "fyang@hotmail.com"
    is_premium = True  # Asumsikan semua pengguna premium untuk contoh ini
    error_message = None
    success_message = None

    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO marmut.downloaded_song (id_song, email_downloader) VALUES (%s, %s);", 
                               [song_id, email_downloader])
            success_message = "Lagu berhasil diunduh!"
        except Exception as e:
            error_message = str(e)

    # Konteks template
    context = {
        'playlist_id': playlist_id,
        'song_id': song_id,
        'error_message': error_message,
        'success_message': success_message,
        'is_premium': is_premium
    }

    return render(request, 'play_song.html', context)

