import logging
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
from django.http import JsonResponse,HttpResponseRedirect
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
# Create your views here.

def dashboard(request):
    # Ambil data pengguna dari session
    user_data = request.session.get('user_data', {})

    # Initialize role flags
    user_data.update({
        'is_artist': False,
        'is_songwriter': False,
        'is_podcaster': False,
        'is_label': False,
        'is_pengguna': False,
        'is_premium' : False,
        'roles': [],
        

    })
    #cek apakah dia premium atau tidak di table premium
    query_premium = f"SELECT 1 FROM marmut.premium WHERE email = '{user_data.get('email')}'"
    with connection.cursor() as cursor:
        cursor.execute(query_premium)
        user_data['is_premium'] = cursor.fetchone() is not None
    
    # Check for Artist
    query_artist = f"SELECT 1 FROM marmut.artist WHERE email_akun = '{user_data.get('email')}'"
    with connection.cursor() as cursor:
        cursor.execute(query_artist)
        user_data['is_artist'] = cursor.fetchone() is not None
        user_data['roles'].append('Artist') if user_data['is_artist'] else ''

    # Check for Pengguna
    query_pengguna = f"SELECT 1 FROM marmut.akun WHERE email = '{user_data.get('email')}'"
    with connection.cursor() as cursor:
        cursor.execute(query_pengguna)
        user_data['is_pengguna'] = cursor.fetchone() is not None
        user_data['roles'].append('Pengguna') if user_data['is_pengguna'] else ''

    # Check for Songwriter
    query_songwriter = f"SELECT 1 FROM marmut.songwriter WHERE email_akun = '{user_data.get('email')}'"
    with connection.cursor() as cursor:
        cursor.execute(query_songwriter)
        user_data['is_songwriter'] = cursor.fetchone() is not None
        user_data['roles'].append('Songwriter') if user_data['is_songwriter'] else ''

    # Check for Podcaster
    query_podcaster = f"SELECT 1 FROM marmut.podcaster WHERE email = '{user_data.get('email')}'"
    with connection.cursor() as cursor:
        cursor.execute(query_podcaster)
        user_data['is_podcaster'] = cursor.fetchone() is not None
        user_data['roles'].append('Podcaster') if user_data['is_podcaster'] else ''

    # Check for Label
    query_label = f"SELECT 1 FROM marmut.label WHERE email = '{user_data.get('email')}'"
    with connection.cursor() as cursor:
        cursor.execute(query_label)
        user_data['is_label'] = cursor.fetchone() is not None
        user_data['roles'].append('Label') if user_data['is_label'] else ''

    # Update session with user_data
    user_data['is_logged_in'] = any([user_data['is_artist'], user_data['is_songwriter'], user_data['is_podcaster'], user_data['is_label'], user_data['is_pengguna']])
    print("cekk")
    print(user_data['is_logged_in'])
    request.session['user_data'] = user_data

    # Query to get user info
    if user_data.get('is_label'):
        query_info = f"""
            SELECT nama, email, kontak
            FROM marmut.label
            WHERE email = '{user_data.get('email')}'
        """
    else:
        query_info = f"""
            SELECT email, nama, kota_asal, gender, tempat_lahir, tanggal_lahir
            FROM marmut.akun
            WHERE email = '{user_data.get('email')}'
        """

    with connection.cursor() as cursor:
        cursor.execute(query_info)
        columns = [col[0] for col in cursor.description]
        user_info = dict(zip(columns, cursor.fetchone()))

    playlists = []
    songs_artist = []
    songs_songwriter = []
    podcasts = []
    albums = []

    # Contoh query untuk pengguna biasa
    if not user_data.get('is_label'):
        query_playlists = f"""
            SELECT judul
            FROM marmut.user_playlist
            WHERE email_pembuat = '{user_data.get('email')}'
        """
        with connection.cursor() as cursor:
            cursor.execute(query_playlists)
            playlists = [row[0] for row in cursor.fetchall()]

    # Kalau dia artist
    if user_data.get('is_artist'):
        query_songs_artist = f"""
            SELECT k.judul
            FROM marmut.konten k
            JOIN marmut.song s ON k.id = s.id_konten
            JOIN marmut.artist a ON s.id_artist = a.id
            WHERE a.email_akun = '{user_data.get('email')}'
        """
        with connection.cursor() as cursor:
            cursor.execute(query_songs_artist)
            songs_artist = [row[0] for row in cursor.fetchall()]

    # Kalau dia songwriter
    if user_data.get('is_songwriter'):
        query_songs_songwriter = f"""
            SELECT k.judul
            FROM marmut.konten k
            JOIN marmut.songwriter_write_song sws ON k.id = sws.id_song
            JOIN marmut.songwriter sw ON sws.id_songwriter = sw.id
            WHERE sw.email_akun = '{user_data.get('email')}'
        """
        with connection.cursor() as cursor:
            cursor.execute(query_songs_songwriter)
            songs_songwriter = [row[0] for row in cursor.fetchall()]

    # Kalau dia podcaster
    if user_data.get('is_podcaster'):
        query_podcasts = f"""
            SELECT k.judul
            FROM marmut.konten k
            JOIN marmut.podcast p ON k.id = p.id_konten
            WHERE p.email_podcaster = '{user_data.get('email')}'
        """
        with connection.cursor() as cursor:
            cursor.execute(query_podcasts)
            podcasts = [row[0] for row in cursor.fetchall()]

    # Kalau dia label
    if user_data.get('is_label'):
        query_albums = f"""
            SELECT a.judul
            FROM marmut.album a
            JOIN marmut.label l ON a.id_label = l.id
            WHERE l.email = '{user_data.get('email')}'
        """
        with connection.cursor() as cursor:
            cursor.execute(query_albums)
            albums = [row[0] for row in cursor.fetchall()]

    context = {
        'user_data': user_info,
        'playlists': playlists,
        'songs_artist': songs_artist,
        'songs_songwriter': songs_songwriter,
        'podcasts': podcasts,
        'albums': albums
    }
    print(user_data)
    print("albummmm")
    print(albums)

    return render(request, 'dashboard.html', context)

#coba yang baru login nya
@csrf_exempt
def login_with_postgres(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        
        # Query untuk mencari pengguna atau label berdasarkan email dan mengambil passwordnya
        query_akun = f"SELECT email, password, nama FROM marmut.akun WHERE email = %s"
        query_label = f"SELECT email, password, nama FROM marmut.label WHERE email = %s"

        user_akun = None

        with connection.cursor() as cursor:
            cursor.execute(query_akun, [email])
            user_akun = cursor.fetchone()

            if not user_akun:
                cursor.execute(query_label, [email])
                user_akun = cursor.fetchone()

            if user_akun:
                email, stored_password, nama = user_akun

                # Check if the provided password matches the stored password
                if stored_password == password:
                    # Check for roles
                    queries = {
                        'is_artist': f"SELECT 1 FROM marmut.artist WHERE email_akun = %s",
                        'is_songwriter': f"SELECT 1 FROM marmut.songwriter WHERE email_akun = %s",
                        'is_podcaster': f"SELECT 1 FROM marmut.podcaster WHERE email = %s",
                    }
                    roles = {}
                    for role, query in queries.items():
                        cursor.execute(query, [email])
                        roles[role] = cursor.fetchone() is not None

                    # Check if the user is a label
                    is_label = False
                    cursor.execute(query_label, [email])
                    if cursor.fetchone():
                        is_label = True

                    # Set user data in session
                    request.session['user_data'] = {
                        'email': email,
                        'nama': nama,
                        'is_premium': False,  # Modify this if you need to set it dynamically
                        'is_artist': roles.get('is_artist', False),
                        'is_songwriter': roles.get('is_songwriter', False),
                        'is_podcaster': roles.get('is_podcaster', False),
                        'is_label': is_label,
                        'is_logged_in': True,
                        'roles': roles
                    }

                    user_data = request.session['user_data']
                    email = user_data['email']
                    cursor.execute("SELECT * FROM marmut.premium WHERE email = %s", (email,))
                    prem_flag = cursor.fetchone()
                    print(email)
                    print(prem_flag)
                    # Jika None -> non prem

                    # Jika pengguna premium
                    if (prem_flag):
                        email = prem_flag[0]
                        query = """
                                SELECT *
                                FROM marmut.transaction
                                WHERE email = %s
                                ORDER BY timestamp_dimulai DESC
                                LIMIT 1;
                                """
                        cursor.execute(query, (email,))
                        latest_transaction = cursor.fetchone()

                        if latest_transaction:
                            timestamp_berakhir = latest_transaction[4]
                            if timestamp_berakhir < datetime.datetime.now():
                                cursor.execute("DELETE FROM marmut.downloaded_song WHERE email_downloader = %s", (email,))
                                cursor.execute("DELETE FROM marmut.premium WHERE email = %s", (email,))
                                cursor.execute("INSERT INTO marmut.nonpremium (email) VALUES (%s)", (email,))
                            else:
                                user_data['is_prem'] = True
                                
                    
                    print("\n================ DEBUG AREA ================")
                    print(request.session['user_data'])
                    print("\n")
                    user_data = request.session['user_data']
                    for key, value in user_data.items():
                        print(key + ": " + str(value))
                    print("================ DEBUG AREA ================\n")
                    
                    return redirect('akun:dashboard')
                else:
                    messages.error(request, 'Maaf, password yang Anda masukkan salah.')
            else:
                messages.error(request, 'Pengguna tidak ditemukan.')

    return render(request, "login.html")

#show_home
def home(request):
    return render(request, 'home.html')

#register yang dasar
def register_choice(request):
    return render(request, 'register_choice.html')

#register label 
def register_label(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        nama = request.POST.get('nama')
        kontak = request.POST.get('kontak')

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO marmut.label (email, password, nama, kontak)
                VALUES (%s, %s, %s, %s)
            """, [email, password, nama, kontak])

        return redirect('~/akun/login')  # Ubah 'login' sesuai dengan nama URL untuk halaman login

    return render(request, 'register_label.html')

#register pengguna 
@csrf_exempt
def register_pengguna(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        nama = request.POST.get('nama')
        gender = request.POST.get('gender')
        tempat_lahir = request.POST.get('tempat_lahir')
        tanggal_lahir = request.POST.get('tanggal_lahir')
        kota_asal = request.POST.get('kota_asal')
        roles = request.POST.getlist('role')
        is_verified = True
        #id pemilik hak cipta berarti gapapa None
        id_pemilik_hak_cipta = None
        
        #next : mungkin nanti baru ada triggernya 
        #kalau ga ada role yang dipilih 
        if not roles:
            #maka akan dibuat akund enagn status unverfied
            #dan dikategorikan sebagai pengguna biasa
            #langsung add ke database dulu
            is_verified = False
        with connection.cursor() as cursor:
            #next perlu distrip ga ya?
            cursor.execute("""
                INSERT INTO marmut.akun (email, password, nama, gender, tempat_lahir, tanggal_lahir, is_verified, kota_asal)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, [email, password, nama, gender, tempat_lahir, tanggal_lahir, is_verified, kota_asal])
       
            #tambahkan di table  masing masing role    
            #tambahkan jika podcaster
            if 'podcaster' in roles:
                #attribut hanya email saja
                #karena sudah ada emailnya di table akun, harusnya emailnya bisa langsung tanpa perlu fk lagi 
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO marmut.podcaster (email)
                        VALUES (%s)
                    """, [email])
            
            #tambahkan jika artist
                #note kalau FK berarti data tersebut harus ada di tabel yang di FKan terlebih dahulu
                #jadi asumsinya sudah ada 
            #attributnya ada id dari UUID PK
            #ada email_akun yang FK ke AKUN.email
            #ada id_pemilik_hak_cipta dengan tipe data UUID , yang FK ke pemilik_hak_cipta.id

            #next harusnya bisa -> tanyain -> krn pemilik hak cipta kan dibuat independen 
            if 'artist' in roles:
                artist_id = uuid.uuid4()
                cursor.execute("""SELECT * FROM marmut.akun WHERE email = %s LIMIT 1;""", [email])
                email_akun = cursor.fetchall()
                #ambil email dari table akun
                email_akun = email_akun[0][0] #NEXT
                #ambil id dari table pemilik hak cipta
                # cursor.execute("""  SELECT DISTINCT r.id_pemilik_hak_cipta 
                #                FROM song s
                #                JOIN royalti r ON s.id_konten = r.id_song
                #                WHERE s.id_artist = %s;""", [artist_id])
                # id_pemilik_hak_cipta = cursor.fetchall()
                
                #masukkan ke table artist
                query_insert_artist = """
                INSERT INTO marmut.artist (id, email_akun, id_pemilik_hak_cipta)
                VALUES (%s, %s, %s)
                """
                cursor.execute(query_insert_artist, (artist_id, email_akun, id_pemilik_hak_cipta))
                
            
            #cek di dataset apakah ada orang yang id song writernya sama dengan id artist 
            #tapi ada kemungkinan kalau satu orang kan bisa jadi artist dan bisa jadi songwriter harusnya saling berbagi id?
            #cek dataset -> 
                #pakai 
               # SELECT * FROM ARTIST WHERE ARTIST.id in (SELECT id FROM SONGWRITER); -> idnya ga ada yg sama antara di kedua table itu
               # SELECT * FROM ARTIST WHERE ARTIST.email_akun in (SELECT email_akun FROM SONGWRITER); -> tapiii ada email yang sama 
            #asumsi: ini berarti untuk satu orangyag rolenya bisa artist dan songwriter maka idnya berbeda, tetapi email_akunnya boleh sama

            #tambahkan jika songwriter
            if 'songwriter' in roles:
                songwriter_id = uuid.uuid4()
                cursor.execute("""SELECT * FROM marmut.akun WHERE email = %s LIMIT 1;""", [email])
                email_akun = cursor.fetchall()
                #ambil email dari table akun
                email_akun = email_akun[0][0] #NEXT
                #ambil id pemilik hak cipta -> ambil dari songwriter_write_song dulu baru dapat id_songnya 
                # query = """
                #     SELECT DISTINCT r.id_pemilik_hak_cipta
                #     FROM songwriter_write_song sws
                #     JOIN song s ON sws.id_song = s.id_konten
                #     JOIN royalti r ON s.id_konten = r.id_song
                #     WHERE sws.id_songwriter = %s
                # """
                # cursor.execute(query, (artist_id,))
                # id_pemilik_hak_cipta = cursor.fetchone()
                
                #masukkan ke table artist
                query_insert_artist = """
                INSERT INTO marmut.songwriter (id, email_akun, id_pemilik_hak_cipta)
                VALUES (%s, %s, %s)
                """
                cursor.execute(query_insert_artist, (songwriter_id, email_akun, id_pemilik_hak_cipta))
            
            return HttpResponseRedirect('/akun/login/') 
            # except psycopg2.Error as error:
            #     messages.error(request, f'{error}')
            # except Exception as error:
            #     messages.error(request, f'{error}')
    return render(request, 'register_pengguna.html')

logger = logging.getLogger(__name__)

def logout_view(request):
    # Cetak nama pengguna sebelum menghapus sesi
    logger.info(f"Nama pengguna sebelum logout: {request.session.get('username')}")

    # Hapus data sesi
    request.session.flush()

    # Cetak nama pengguna setelah menghapus sesi
    logger.info(f"Nama pengguna setelah logout: {request.session.get('username')}")

    # Redirect ke halaman login
    return redirect('akun:login')