from django.shortcuts import render, redirect
import psycopg2
from django.db import connection

# Create your views here.
def show_cari_konten(request):
    user_data = request.session.get('user_data', {})
    if 'query' in request.GET:
        query = request.GET['query']
        return redirect(f'/search/{query}')
    
    return render(request, "cari_konten.html")

def show_hasil_cari(request, judul):
    user_data = request.session.get('user_data', {})
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
        return render(request, "hasil_cari.html", context)
    else:
        return render(request, "hasil_cari_not_found.html", context)