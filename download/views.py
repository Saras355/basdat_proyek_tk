from django.shortcuts import render, redirect
import psycopg2
from django.db import connection

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
    return render(request, "downloaded_song.html", context)

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
    return render(request, "delete_song.html", context)