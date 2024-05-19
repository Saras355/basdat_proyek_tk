from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
import uuid
# from .forms import LoginForm -> ga usah pakai form langsung dari login.html aja(?)
import json
from django.db import connection
# from connect_postgres import execute_sql_query
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
import datetime
import uuid
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.urls import reverse
import psycopg2
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection


# #CREATE ALBUM -> butuh masukkin judul isian, dan dropdown label (fetch semua label yang terdaftar di marmut)
# def get_labels():
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT id, name FROM marmut_label")
#         labels = cursor.fetchall()
#     return [{'id': label[0], 'name': label[1]} for label in labels]

# def create_album(request):
#     if request.method == 'POST':
#         judul = request.POST.get('judul')
#         label_id = request.POST.get('label')
#         album_id = str(uuid.uuid4()) 
#         with connection.cursor() as cursor:
#             cursor.execute("""
#                 INSERT INTO marmut_album (id, judul, label_id) 
#                 VALUES (%s, %s, %s)
#             """, [album_id, judul, label_id])
#         #cek lagi yang relate dengan table album -> song ga relate karena kan bisa aja albumnya kosong dulu -> jumlah lagunya 0 misalnya
#         #
#         return redirect(reverse('success_create_album'))
    
#     labels = get_labels()
#     return render(request, 'create_album.html', {'labels': labels})
    

# def success_create_album(request):
#     return HttpResponse("Album anda berhasil dibuat! Terus berkarya")


# #LIST_ALBUM VIEWS
# def get_albums():
#     with connection.cursor() as cursor:
#         cursor.execute("""
#             SELECT a.id, a.judul, l.name as label_name,
#                    COUNT(s.id) as jumlah_lagu,
#                    COALESCE(SUM(s.durasi), 0) as total_durasi
#             FROM marmut_album a
#             LEFT JOIN marmut_label l ON a.label_id = l.id
#             LEFT JOIN marmut_song s ON a.id = s.album_id
#             GROUP BY a.id, a.judul, l.name
#         """)
#         albums = cursor.fetchall()
#     return [{
#         'id': album[0],
#         'judul': album[1],
#         'label_name': album[2],
#         'jumlah_lagu': album[3],
#         'total_durasi': album[4]
#     } for album in albums]

# def list_album(request):
#     albums = get_albums() #ambil semua album
#     return render(request, 'list_album.html', {'albums': albums})

# def hapus_album(request, album_id):
#     if request.method == 'POST':
#         with connection.cursor() as cursor:
#             cursor.execute("DELETE FROM marmut_album WHERE id = %s", [album_id])
#         return redirect(reverse('list_album'))
# #function get album by id bisa untuk list album dan untuk list lagu di suatu album  
# def get_album_by_id(album_id):
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT id, judul FROM marmut_album WHERE id = %s", [album_id])
#         album = cursor.fetchone()
#     return {'id': album[0], 'judul': album[1]} if album else None

# #lanjutan dari list_album views


# #create_lagu views
#     #ambil bedasarkanalbum yang diklik -> di album : nama album 



# def get_artists():
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT id, name FROM marmut_artist")
#         artists = cursor.fetchall()
#     return [{'id': artist[0], 'name': artist[1]} for artist in artists]

# def get_songwriters():
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT id, name FROM marmut_songwriter")
#         songwriters = cursor.fetchall()
#     return [{'id': songwriter[0], 'name': songwriter[1]} for songwriter in songwriters]

# def get_genres():
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT id, name FROM marmut_genre")
#         genres = cursor.fetchall()
#     return [{'id': genre[0], 'name': genre[1]} for genre in genres]

# def create_lagu(request):
#     user_data = request.session.get('user_data', {})
#     is_artist = user_data.get('is_artist', False)
#     is_songwriter = user_data.get('is_songwriter', False)
#     user_artist_id = user_data.get('artist_id', None)
#     user_songwriter_id = user_data.get('songwriter_id', None)
    
#     if request.method == 'POST':
#         album_id = request.POST.get('album')
#         judul = request.POST.get('judul')
#         artist_id = user_artist_id if is_artist else request.POST.get('artist')
#         songwriters = request.POST.getlist('songwriters')
#         genres = request.POST.getlist('genres')
#         durasi = request.POST.get('durasi')
#         song_id = str(uuid.uuid4())

#         with connection.cursor() as cursor:
#             cursor.execute("""
#                 INSERT INTO marmut_song (id, judul, artist_id, album_id, durasi)
#                 VALUES (%s, %s, %s, %s, %s)
#             """, [song_id, judul, artist_id, album_id, durasi])
            
#             for songwriter_id in songwriters:
#                 cursor.execute("""
#                     INSERT INTO marmut_songwriter_write_song (songwriter_id, song_id)
#                     VALUES (%s, %s)
#                 """, [songwriter_id, song_id])
            
#             for genre_id in genres:
#                 cursor.execute("""
#                     INSERT INTO marmut_song_genre (song_id, genre_id)
#                     VALUES (%s, %s)
#                 """, [song_id, genre_id])

#         return redirect(reverse('success'))

#     albums = get_albums()
#     artists = get_artists() if is_songwriter else []
#     songwriters = get_songwriters()
#     genres = get_genres()

#     context = {
#         'albums': albums,
#         'artists': artists,
#         'songwriters': songwriters,
#         'genres': genres,
#         'is_artist': is_artist,
#         'is_songwriter': is_songwriter,
#         'user_artist_id': user_artist_id,
#         'user_songwriter_id': user_songwriter_id,
#     }

#     return render(request, 'create_lagu.html', context)

# #list lagu views

# from django.shortcuts import render, redirect, get_object_or_404
# from django.urls import reverse
# from django.db import connection
# from django.http import HttpResponse

# def get_album_by_id(album_id):
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT id, judul FROM marmut_album WHERE id = %s", [album_id])
#         album = cursor.fetchone()
#     return {'id': album[0], 'judul': album[1]} if album else None

# def get_lagu_by_album_id(album_id):
#     with connection.cursor() as cursor:
#         cursor.execute("""
#             SELECT id, judul, durasi, total_play, total_download
#             FROM marmut_song
#             WHERE album_id = %s
#         """, [album_id])
#         lagu_list = cursor.fetchall()
#     return [{
#         'id': lagu[0],
#         'judul': lagu[1],
#         'durasi': lagu[2],
#         'total_play': lagu[3],
#         'total_download': lagu[4]
#     } for lagu in lagu_list]

# def list_lagu(request, album_id):
#     album = get_album_by_id(album_id)
#     if not album:
#         return HttpResponse("Album not found", status=404)

#     lagu_list = get_lagu_by_album_id(album_id)

#     context = {
#         'album': album,
#         'lagu_list': lagu_list
#     }
#     return render(request, 'list_lagu.html', context)

# def hapus_lagu(request, lagu_id):
#     if request.method == 'POST':
#         with connection.cursor() as cursor:
#             cursor.execute("DELETE FROM marmut_song WHERE id = %s", [lagu_id])
#         return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
#     return HttpResponse(status=405)

# def lihat_detail(request, lagu_id):
#     with connection.cursor() as cursor:
#         cursor.execute("""
#             SELECT id, judul, durasi, total_play, total_download, artist_id
#             FROM marmut_song
#             WHERE id = %s
#         """, [lagu_id])
#         lagu = cursor.fetchone()

#     if not lagu:
#         return HttpResponse("Lagu not found", status=404)

#     context = {
#         'lagu': {
#             'id': lagu[0],
#             'judul': lagu[1],
#             'durasi': lagu[2],
#             'total_play': lagu[3],
#             'total_download': lagu[4],
#             'artist_id': lagu[5]
#         }
#     }
#     return render(request, 'lihat_detail.html', context)


#CEK_ROYALTI views.py
def cek_royalti(request):
    # Raw query to retrieve royalty information
    user_data = request.session.get('user_data', {})
    user_email = user_data.get('email', '')
    royalti_artist = []
    royalti_songwriter = []
    royalti_label = []


    #semuanya -> label, songwriter, dan artist -> ada pemilih hak cipta kan
    #cari terlebih dahulu id pemilik_hak_ciptanya
    #if is_label -> cari dari table label
    if user_data['is_label']:
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT id FROM marmut.label WHERE email = %s
            """, [user_email])
            label_hak_cipta_id = cursor.fetchall()
            print("Keprinttt")
            print(label_hak_cipta_id)
    #if is_artist -> cari dari table artist
    if user_data['is_artist']:
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT id FROM marmut.artist WHERE email_akun = %s
            """, [user_email])
            artist_hak_cipta_id = cursor.fetchall()
    #if is_songwriter -> cari dari table songwriter
    if user_data['is_songwriter']:
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT id FROM marmut.songwriter WHERE email_akun = %s
            """, [user_email])
            songwriter_hak_cipta_id = cursor.fetchall()
        
    #krn bisa multiple role -> berarti di html pakai as artist , or as sonrgwritre, dan seterunsya 
    #ambil dulu sebagai label
    if user_data['is_artist']:
        with connection.cursor() as cursor:
            cursor.execute("""
            SET SEARCH_PATH TO MARMUT;
            SELECT 
            k.judul AS judul_lagu,
            Al.judul AS judul_album,
            S.total_play AS TotalPlay,
            S.total_download AS TotalDownload,
            (CAST(S.total_play AS NUMERIC) * CAST(PHC.rate_royalti AS NUMERIC)) AS TotalRoyalti,
            PHC.id AS id_pemilik_hak_cipta,
            S.id_konten AS id_song
            FROM
            ARTIST a
            JOIN PEMILIK_HAK_CIPTA AS PHC On phc.id = A.id_pemilik_hak_cipta
            
            JOIN SONG as s on a.id = s.id_artist
            JOIN KONTEN K ON K.id = S.id_konten
            JOIN ALBUM Al ON al.id = s.id_album
            WHERE
            a.email_akun = %s;

            """, [user_email])
            royalti_artist = cursor.fetchall()
            #JOIN ROYALTI AS R on r.id_pemilik_hak_cipta = a.id_pemilik_hak_cipta
            #krn ini ada yg ga diamsukkin ke royalti
            for row in royalti_artist:
                id_song = row[6]
                id_pemilik_hak_cipta = row[5]
                total_royalti = row[4]

                cursor.execute("""
                UPDATE ROYALTI
                SET jumlah = %s
                WHERE id_pemilik_hak_cipta = %s AND id_song = %s
                """, [total_royalti/10000, id_pemilik_hak_cipta, id_song])
            print("ROYALTI ARTIS")
            print(royalti_artist)

    # #if is_songwriter
    if user_data['is_songwriter']:
        print("USERRRRRRRRRRRRRRR EMAILLLLLLLLLLLL SONGWRITERR")
        print(user_email)
        with connection.cursor() as cursor:
            cursor.execute("""
            
                SET SEARCH_PATH TO MARMUT;
                SELECT 
                k.judul AS judul_lagu,
                Al.judul AS judul_album,
                S.total_play AS TotalPlay,
                S.total_download AS TotalDownload,
                (CAST(S.total_play AS NUMERIC) * CAST(PHC.rate_royalti AS NUMERIC)) AS TotalRoyalti,
                PHC.id AS id_pemilik_hak_cipta,
                s.id_konten AS id_song
                FROM
                SONGWRITER a
                JOIN songwriter_write_song as sw on a.id = sw.id_songwriter
                JOIN PEMILIK_HAK_CIPTA AS PHC On phc.id = A.id_pemilik_hak_cipta
               
                JOIN song as s on s.id_konten = sw.id_song
              
      
                JOIN KONTEN K ON K.id = S.id_konten
                JOIN ALBUM Al ON al.id = s.id_album
                WHERE
                a.email_akun = %s;

            """, [user_email])
            royalti_songwriter = cursor.fetchall()
            #ini karena ternyata ada yang belum diamsukkin ke royalti
             # JOIN ROYALTI AS R on r.id_pemilik_hak_cipta = a.id_pemilik_hak_cipta
            for row in royalti_songwriter:
                id_song = row[6]
                id_pemilik_hak_cipta = row[5]
                total_royalti = row[4]

                cursor.execute("""
                UPDATE ROYALTI
                SET jumlah = %s
                WHERE id_pemilik_hak_cipta = %s AND id_song = %s
                """, [total_royalti/10000, id_pemilik_hak_cipta, id_song])
 

    # #if is_songwriter
    if user_data['is_label']:
        with connection.cursor() as cursor:
            cursor.execute("""
            SET SEARCH_PATH TO MARMUT;
            SELECT
            k.judul AS judul_lagu,
            A.judul AS judul_album,
            S.total_play AS TotalPlay,
            S.total_download AS TotalDownload,
            (CAST(S.total_play AS NUMERIC) * CAST(PHC.rate_royalti AS NUMERIC)) AS TotalRoyalti,
            PHC.id AS id_pemilik_hak_cipta,
            s.id_konten as id_song
            FROM
            LABEL L
            JOIN ALBUM A ON L.id = A.id_label
            JOIN SONG S ON S.id_album = A.id
            JOIN KONTEN K ON K.id = S.id_konten
            JOIN PEMILIK_HAK_CIPTA PHC ON L.id_pemilik_hak_cipta = PHC.id
            WHERE
            L.email = %s

            """, [user_email])
            royalti_label = cursor.fetchall()
            print(royalti_label)
            for row in royalti_label:
                id_song = row[6]
                id_pemilik_hak_cipta = row[5]
                total_royalti = row[4]

                cursor.execute("""
                UPDATE ROYALTI
                SET jumlah = %s
                WHERE id_pemilik_hak_cipta = %s AND id_song = %s
                """, [total_royalti/10000, id_pemilik_hak_cipta, id_song])
    print("royalti artist")
    print(royalti_artist)
    print("royalti_songwriter")
    print(royalti_songwriter)
    print("royalti_label")
    print(royalti_label)
    context = {
        'royalti_artist': royalti_artist,
        'royalti_songwriter': royalti_songwriter,
        'royalti_label': royalti_label

    }
    return render(request, 'cek_royalti.html', context)

# SET SEARCH_PATH TO MARMUT;
#             SELECT a.judul AS JudulLagu, A.judul AS JudulAlbum, S.total_play AS TotalPlay, 
#             S.total_download AS TotalDownload, 
#             (CAST(S.total_play AS NUMERIC) * CAST(PH.rate_royalti AS NUMERIC)) AS TotalRoyalti
#             FROM SONG AS S
#             JOIN ALBUM AS A ON S.id_album = A.id
#             JOIN ARTIST AS AR ON S.id_artist = AR.id
#             JOIN PEMILIK_HAK_CIPTA AS PH ON AR.id_pemilik_hak_cipta = PH.id
#             WHERE AR.email_akun = %s



from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db import connection
from django.urls import reverse
import uuid

def list_album(request):
    user_data = request.session.get('user_data', {})
    is_label = user_data.get('is_label', False)
    user_email = user_data.get('email', None)

    if not is_label:
        return HttpResponse("You are not authorized to access this page", status=403)

    #ambil id label dari email
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM marmut.label WHERE email = %s", [user_email])
        label_id = cursor.fetchone()[0]
    
    with connection.cursor() as cursor:
        cursor.execute("""
           SELECT
                ALBUM.id,
                ALBUM.judul,
                ALBUM.jumlah_lagu,
                ALBUM.total_durasi
            FROM
                marmut.ALBUM
            JOIN
                marmut.LABEL ON ALBUM.id_label = LABEL.id
            WHERE
                LABEL.id = %s;
        """, [label_id])
        album_list = cursor.fetchall()


    context = {
        'album_list': [{
            'id': album[0],
            'judul': album[1],
            'jumlah_lagu': album[2],
            'total_durasi': album[3]
        } for album in album_list]
    }
    return render(request, 'list_album.html', context)

def list_album_artist(request):
    user_data = request.session.get('user_data', {})
    email = user_data.get('email', None)
    is_artist = user_data.get('is_artist', False)
    is_songwriter = user_data.get('is_songwriter', False)
    is_label = user_data.get('is_label', False)

    if not (is_artist or is_songwriter or is_label):
        return HttpResponse("You are not authorized to access this page", status=403)

    album_list_songwriter = []
    album_list_artist = []

    if is_songwriter:
        with connection.cursor() as cursor:
            cursor.execute("""
                SET SEARCH_PATH TO MARMUT;
                SELECT a.id, a.judul, a.jumlah_lagu, a.total_durasi, l.nama
                FROM songwriter sw
                JOIN songwriter_write_song sws ON sw.id = sws.id_songwriter
                JOIN song s ON sws.id_song = s.id_konten
                JOIN album a ON s.id_album = a.id
                JOIN label l ON a.id_label = l.id
                WHERE sw.email_akun = %s
            """, [email])
            album_list_songwriter = cursor.fetchall()
    album_list_songwriter = list(set(album_list_songwriter))
    if is_artist:
        with connection.cursor() as cursor:
            cursor.execute("""
                SET SEARCH_PATH TO MARMUT;
                SELECT DISTINCT a.id, a.judul, a.jumlah_lagu, a.total_durasi, l.nama
                FROM artist ar
                JOIN song s ON ar.id = s.id_artist
                JOIN album a ON s.id_album = a.id
                JOIN label l ON a.id_label = l.id
                WHERE ar.email_akun = %s
            """, [email])
            album_list_artist = cursor.fetchall()

    context = {
        'album_list_songwriter': [{
            'id': album[0],
            'judul': album[1],
            'jumlah_lagu': album[2],
            'total_durasi': album[3],
            'label': album[4]
        } for album in album_list_songwriter],
        'album_list_artist': [{
            'id': album[0],
            'judul': album[1],
            'jumlah_lagu': album[2],
            'total_durasi': album[3],
            'label': album[4]
        } for album in album_list_artist]
    }
    return render(request, 'list_album_artist.html', context)



def daftar_lagu(request, album_id):
    with connection.cursor() as cursor:
        #cursor.execute("SELECT id_konten, judul, durasi, total_play, total_download FROM marmut.song WHERE id_album = %s", [album_id])
        cursor.execute("""SELECT id_konten, k.judul, k.durasi, total_play, total_download 
                       FROM marmut.song
                       JOIN marmut.konten k ON song.id_konten = k.id
                       WHERE id_album = %s """, [album_id])

        song_list = cursor.fetchall()
        
        cursor.execute("SELECT judul FROM marmut.album WHERE id = %s", [album_id])
        album = cursor.fetchone()

    context = {
        'album': {'judul': album[0]},
        'song_list': [{
            'id': song[0],
            'judul': song[1],
            'durasi': song[2],
            'total_play': song[3],
            'total_download': song[4]
        } for song in song_list]
    }
    return render(request, 'daftar_lagu.html', context)
def lihat_detail_lagu(request, song_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id_konten, judul, durasi, total_play, total_download
            FROM marmut.song
            JOIN marmut.konten ON song.id_konten = konten.id
            WHERE id_konten = %s
        """, [song_id])
        song = cursor.fetchone()

    if not song:
        return HttpResponse("Lagu not found", status=404)

    context = {
        'song': {
            'id': song[0],
            'judul': song[1],
            'durasi': song[2],
            'total_play': song[3],
            'total_download': song[4]
        }
    }
    return render(request, 'lihat_detail_lagu.html', context)

#BATASSSSSSS
#BATASSSSSS


def create_album(request):
    user_data = request.session.get('user_data', {})
    email = user_data.get('email', None)
 
    if request.method == "POST":
        #print(request.POST)
        for a in request.POST:
            print(a, request.POST[a])
        judul_album = request.POST.get('judul_album')
        label_str = request.POST.get('label')
        label_id = label_str[13:49]
        judul_lagu = request.POST.get('judul_lagu')
        artists = request.POST.get('artist')
        print(artists)
        songwriters = request.POST.getlist('songwriter[]')
        genres = request.POST.getlist('genre[]')
        durasi = request.POST.get('durasi')
        #ambil tanggal sekarang
        tanggal_rilis = datetime.datetime.now()
        tahun = tanggal_rilis.year
        
        #carik artist email di database akun
        with connection.cursor() as cursor:
            cursor.execute("SELECT email FROM marmut.akun WHERE nama = %s", [artists])
            artist_email = cursor.fetchone()
            print("AARTISTTTTTTTTTTTTTTTT EMAILLLLLLLLLLLLLL")
            print(artist_email)
        print("YANG INIIIII KEPRINTTT")
        #carik di artist_id pakai query dah 
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM marmut.artist WHERE email_akun = %s", [artist_email])
            artist_id = cursor.fetchone()
        
        print(artist_id)
        
        genre_masuk = []
        #isinya nomor idnya 
        for genre in genres:
            print(genre)
            with connection.cursor() as cursor:
                cursor.execute("SELECT DISTINCT genre  FROM marmut.genre")
                ada_genre = cursor.fetchall()
                ada_genre = ada_genre[int(genre)]
                ada_genre_2 = ada_genre[0]
                genre_masuk.append(ada_genre_2)
        
       

        #ambil dari nomor genre ke query
        print(songwriters)
        if user_data['is_songwriter']:
            with connection.cursor() as cursor:
                cursor.execute("SELECT DISTINCT id FROM marmut.songwriter WHERE email_akun = %s", (email,))
                songwriter_orangnya = cursor.fetchall()
                songwriters.append(str(songwriter_orangnya[0][0]))
        songwriter_ids = [songwriter for songwriter in songwriters]
        

        #sekarnag bagian insert data ke database
        album_id = str(uuid.uuid4())
        song_id = str(uuid.uuid4())
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO marmut.konten (id, judul,  tanggal_rilis, tahun, durasi) VALUES (%s, %s, %s, %s, %s)", [song_id, judul_lagu, tanggal_rilis, tahun, durasi])
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO marmut.album (id, judul, jumlah_lagu, id_label, total_durasi) VALUES (%s, %s, %s, %s, %s)", [album_id, judul_album, 1, label_id, int(durasi)])
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO marmut.song (id_konten, id_artist, id_album) VALUES (%s, %s, %s)", [song_id, artist_id, album_id])
        with connection.cursor() as cursor:
            for genre_id in genre_masuk:
                cursor.execute("INSERT INTO marmut.genre (id_konten, genre) VALUES (%s, %s)", [song_id, genre_id])
        with connection.cursor() as cursor:
            for songwriter_id in songwriter_ids:
                cursor.execute("INSERT INTO marmut.songwriter_write_song (id_songwriter, id_song) VALUES (%s, %s)", [songwriter_id, song_id])


        #NEXT HABIS INI KAYAKNYA AMBIL SEMUA SYANG BISA PUNYA ROYALTI DAH SEPERTI ARTIST, LABEL, SONGWRITER 
        # TAPI MASALAHNYA RIYALTI NYA GA TAU BERAPAAN
        #return HttpResponse(f'Album {judul_album} berhasil dibuat dengan artist: {label_str}{(artists)}, songwriters: {", ".join(songwriters)}, genres: {", ".join(genres)}, durasi: {durasi} menit.')
        #return ke list album
        return HttpResponseRedirect(reverse('list_album_artist'))
    #ambil labels dulu dari database, sekalian dengan key nya 
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nama FROM marmut.label")
        labels = cursor.fetchall()
        #petakan ke dictionary
        labels = [{'id': label[0], 'nama': label[1]} for label in labels]

        cursor.execute("SELECT id, email_akun FROM marmut.artist")
        artists = cursor.fetchall()
        #petakan ke dictionary
        artists = [{'id': artist[0], 'email_akun': artist[1]} for artist in artists]


        cursor.execute("SELECT id, email_akun FROM marmut.songwriter WHERE email_akun != %s", (email,))
        songwriters = cursor.fetchall()
        #petakan ke dictionary
        songwriters = [{'id': songwriter[0], 'email_akun': songwriter[1]} for songwriter in songwriters]

        cursor.execute("SELECT DISTINCT genre FROM marmut.genre")
        genres = cursor.fetchall()
        #petakan ke dictionary -> enumparate
        genres = [{'id': idx, 'genre': genre[0]} for idx, genre in enumerate(genres)]
        
        print(genres)
        print(labels)
        print(songwriters)
        print(artists)
       
    return render(request, 'create_album.html', {
        'labels': labels,
        'artists': artists,
        'songwriters': songwriters,
        'genres': genres,
    })
        
def create_lagu(request, album_id):
    user_data = request.session.get('user_data', {})
    is_artist = user_data.get('is_artist', False)
    is_songwriter = user_data.get('is_songwriter', False)
    email = user_data.get('email', None)
    album_id = album_id
    print("album idnya ")
    print(album_id)
    artist_id = None
    with connection.cursor() as cursor:
                cursor.execute("SELECT judul FROM marmut.album WHERE id = %s", [album_id])
                judul_album = cursor.fetchone()[0]

    #label ambil dari database
    with connection.cursor() as cursor:
        cursor.execute("SELECT label.id, nama FROM marmut.label JOIN marmut.album ON label.id = album.id_label WHERE album.id = %s", [album_id])
        labels = cursor.fetchall()
        #petakan ke dictionary
        labels = [{'id': label[0], 'nama': label[1]} for label in labels]

    label_id = labels[0]['id']
    if request.method == "POST":
            #print(request.POST)
            for a in request.POST:
                print(a, request.POST[a])
            #ambil judul album dari database dari album_id
         
           
            judul_lagu = request.POST.get('judul_lagu')
            artists = request.POST.get('artist')
            print(artists)
            songwriters = request.POST.getlist('songwriter[]')
            genres = request.POST.getlist('genre[]')
            durasi = request.POST.get('durasi')
            #ambil tanggal sekarang
            tanggal_rilis = datetime.datetime.now()
            tahun = tanggal_rilis.year
            
            
            # print("KHUUUUUUUUUUUUUUUUUUUU")
            #carik di artist_id pakai query dah 
            with connection.cursor() as cursor:
                cursor.execute("SELECT artist.id FROM marmut.AKUN JOIN marmut.artist ON akun.email = artist.email_akun WHERE nama = %s", [artists])
                artist_id = cursor.fetchone()
            
            print(artist_id)
            
            genre_masuk = []
            #isinya nomor idnya 
            for genre in genres:
                print(genre)
                with connection.cursor() as cursor:
                    cursor.execute("SELECT DISTINCT genre  FROM marmut.genre")
                    ada_genre = cursor.fetchall()
                    ada_genre = ada_genre[int(genre)]
                    ada_genre_2 = ada_genre[0]
                    genre_masuk.append(ada_genre_2)
            
        

            #ambil dari nomor genre ke query
            print(songwriters)
            if user_data['is_songwriter']:
                print(email)
                with connection.cursor() as cursor:
                    cursor.execute("SELECT  id FROM marmut.songwriter WHERE email_akun = %s", (email,))
                    songwriter_orangnya = cursor.fetchall()
                    songwriters.append(str(songwriter_orangnya[0][0]))
            songwriter_ids = [songwriter for songwriter in songwriters]
            

            #sekarnag bagian insert data ke database
            
            song_id = str(uuid.uuid4())
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO marmut.konten (id, judul,  tanggal_rilis, tahun, durasi) VALUES (%s, %s, %s, %s, %s)", [song_id, judul_lagu, tanggal_rilis, tahun, durasi])
                # cursor.execute("INSERT INTO marmut.album (id, judul, jumlah_lagu, id_label, total_durasi) VALUES (%s, %s, %s, %s, %s)", [album_id, judul_album, 1, label_id, int(durasi)])
            #carik artist lagi gatau kenapa ini jadi null
            # with connection.cursor() as cursor:
            #     cursor.execute("SELECT id FROM marmut.artist WHERE email_akun = %s", [artists])
            #     artist_id = cursor.fetchone()
            #     print("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
            #     print(artist_id)
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO marmut.song (id_konten, id_artist, id_album) VALUES (%s, %s, %s)", [song_id, artist_id, album_id])
                print("album_id cek dua kali")
                print(album_id)
                print(artist_id)
            with connection.cursor() as cursor:
                for genre_id in genre_masuk:
                    cursor.execute("INSERT INTO marmut.genre (id_konten, genre) VALUES (%s, %s)", [song_id, genre_id])
            with connection.cursor() as cursor:
                for songwriter_id in songwriter_ids:
                    print("POOOOOOOOOOOOOOOOOOOOOOOOOOOOOGGGRHTUI GNRYTUGYWEFTEWFTYYYYYYYYYYY8")
                    print(songwriter_id)
                    cursor.execute("INSERT INTO marmut.songwriter_write_song (id_songwriter, id_song) VALUES (%s, %s)", [songwriter_id, song_id])


            #NEXT HABIS INI KAYAKNYA AMBIL SEMUA SYANG BISA PUNYA ROYALTI DAH SEPERTI ARTIST, LABEL, SONGWRITER 
            # TAPI MASALAHNYA RIYALTI NYA GA TAU BERAPAAN
            #return HttpResponse(f'Album {judul_album} berhasil dibuat dengan artist: {label_str}{(artists)}, songwriters: {", ".join(songwriters)}, genres: {", ".join(genres)}, durasi: {durasi} menit.')
            return redirect('list_album_artist')

           # return redirect(reverse('list_album_artist'))

        #ambil labels dulu dari database, sekalian dengan key nya 
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nama FROM marmut.label")
        labels = cursor.fetchall()
        #petakan ke dictionary
        labels = [{'id': label[0], 'nama': label[1]} for label in labels]

        cursor.execute("SELECT id, email_akun FROM marmut.artist")
        artists = cursor.fetchall()
        #petakan ke dictionary
        artists = [{'id': artist[0], 'email_akun': artist[1]} for artist in artists]


        cursor.execute("SELECT id, email_akun FROM marmut.songwriter WHERE email_akun != %s", (email,))
        songwriters = cursor.fetchall()
        #petakan ke dictionary
        songwriters = [{'id': songwriter[0], 'email_akun': songwriter[1]} for songwriter in songwriters]

        cursor.execute("SELECT DISTINCT genre FROM marmut.genre")
        genres = cursor.fetchall()
        #petakan ke dictionary -> enumparate
        genres = [{'id': idx, 'genre': genre[0]} for idx, genre in enumerate(genres)]
            
        print(genres)
        print(labels)
        print(songwriters)
        print(artists)
    return render(request, 'create_lagu.html', {
        'album_id' : album_id,
        'judul_album': judul_album,
        'labels': labels,
        'artists': artists,
        'songwriters': songwriters,
        'genres': genres,
    }) 

def hapus_album(request, album_id):
    user_data = request.session.get('user_data', {})
    print("iniiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
    print(album_id)
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM marmut.album WHERE id = %s", [album_id])
    if user_data['is_artist'] or user_data['is_songwriter']:
        return redirect(reverse('list_album_artist'))
   
    return redirect(reverse('list_album'))
    #return redirect(reverse('list_album_artist') if 'is_artist' in request.session['user_data'] or 'is_songwriter' in request.session['user_data'] else 'list_album')

def hapus_lagu(request, song_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM marmut.song WHERE id_konten = %s", [song_id])
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


def entry_album_song_create_list(request):
    return render(request, 'entry_album_song_create_list.html')


#tes
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'multiselect_form.html')

def submit(request):
    if request.method == 'POST':
        selected_names = request.POST.getlist('names')
        print("nama yang dipilih")
        print(selected_names)
        return HttpResponse(f'Selected names: {", ".join(selected_names)}')
    return HttpResponse("No data submitted.")
