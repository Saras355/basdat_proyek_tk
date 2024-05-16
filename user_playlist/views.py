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
        with connection.cursor() as cursor:
            cursor.execute(""" 
            INSERT INTO marmut.user_playlist (email_pembuat, judul, deskripsi, jumlah_lagu, tanggal_dibuat, id_user_playlist, id_playlist, total_durasi)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """, ["cburns@gmail.com", judul, deskripsi, 0, datetime.date.today(), str(uuid.uuid4()), id_playlist, 0])
        return redirect('main:show_user_playlist')
    return render(request, 'add_user_playlist.html')

def delete_playlist(request, playlist_id):
    # Hapus user playlist berdasarkan id_playlist
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM marmut.user_playlist WHERE id_playlist = %s;", [playlist_id])
    
    # Hapus playlist berdasarkan id_playlist
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM marmut.playlist WHERE id = %s;", [playlist_id])
    
    # Redirect ke halaman show_user_playlist setelah berhasil menghapus
    return redirect('main:show_user_playlist')

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
            
            return redirect('main:show_user_playlist')
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
    SELECT k.judul, k.durasi, k.tanggal_rilis, ak.nama as oleh
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
        existing_song = query_result(f"""
            SELECT s.* FROM marmut.user_playlist up
            JOIN marmut.playlist_song ps ON ps.id_playlist = up.id_playlist
            JOIN marmut.song s ON ps.id_song = s.id_konten
            WHERE up.id_playlist = '{playlist_id}' AND s.id_konten = '{song_id}';
        """)

        if existing_song:
            return HttpResponse("Lagu sudah ada di dalam playlist", status=400)

        # Add the song to the playlist
        query_result(f"""
            INSERT INTO marmut.playlist_song (id_playlist, id_song)
            VALUES ('{playlist_id}', '{song_id}');
        """)

        return redirect(reverse('detail_user_playlist', args=[playlist_id]))

    # Get the list of all songs for the dropdown
    songs = query_result(f"""
        SELECT s.id_konten, k.judul, a.nama as artist
        FROM marmut.song s
        JOIN marmut.konten k ON s.id_konten = k.id 
        JOIN marmut.artist ar ON s.id_artist = ar.id
        JOIN marmut.akun a ON ar.email_akun = a.email;
    """)

    return render(request, 'add_song.html', {'songs': songs, 'playlist_id': playlist_id})