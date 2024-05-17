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
def list_tables(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'marmut';")
        tables = cursor.fetchall()
        table_list = [table[0] for table in tables]  # Extract table names from tuples
    return render(request, 'list_tables.html', {'tables': table_list})

# def list_tables(request):
#     # with connection.cursor() as cursor:
#     #     cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
#     #     tables = cursor.fetchall()
#     #     table_list = [table[0] for table in tables]  # Extract table names from tuples
#     return render(request, 'akun/list_tables.html')


#membuat untuk views dashboard terlebih dahulu 

# @login_required
# def dashboard(request):
#     #dari request session yang sekarnag -> cek di tiap table apakah emailnya ada atau tidak
#     #ambil request session terlebih dahulu
#     user_data = request.session.get('user_data', {})
#     nama = user_data.get('nama', '')
#     email = user_data.get('email', '')
#     #next apakah is nya bisa ambil dari request session atau harus diquery juga?
#     is_premium = user_data.get('is_premium', False)
#     is_artist = user_data.get('is_artist', False)
#     is_songwriter = user_data.get('is_songwriter', False) #kalau kuncinya ga ada di dalam request.session maka defaultnya jadi False
#     is_podcaster = user_data.get('is_podcaster', False)
#     is_label = user_data.get('is_label', False)
    
#     #is_premium = true -> ini tidak dipakai di dashboard
#     data_dict = {
#         'nama': nama,
#         'email': email,
#     }
#     #is_artist = true

#     #is_songwriter = true
#     #is_podcaster = true
#     #is_label = true
#     return render(request, 'dashboard.html', data_dict)

# #loginnn

# def dashboard(request):
#     user_data = request.session.get('user_data', {})
#     context = {
#         'is_logged_in': user_data.get('is_logged_in', False),
#         'is_premium': user_data.get('is_premium', False),
#         'is_artist': user_data.get('is_artist', False),
#         'is_songwriter': user_data.get('is_songwriter', False),
#         'is_podcaster': user_data.get('is_podcaster', False),
#         'is_label': user_data.get('is_label', False),
#     }
#     return render(request, 'dashboard.html', context)
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

#TEST
# def dashboard(request):
#     # Ambil data pengguna dari session
#     user_data = request.session.get('user_data', {})
#     print(user_data)
#     #{'email': 'jeffrey36@yahoo.com', 'nama': 'Alexis Long', 'is_premium': False, 'is_artist': False, 'is_songwriter': True, 'is_podcaster': False, 'is_label': False}
   
#    #cek apakah dia premium atau tidak di table premium
#     query_premium = f"SELECT 1 FROM marmut.premium WHERE email = '{user_data.get('email')}'"
#     with connection.cursor() as cursor:
#         cursor.execute(query_premium)
#         user_data['is_premium'] = cursor.fetchone() is not None
    
#     #cek apakah dia artist atau tidak di table artist
#     query_artist = f"SELECT 1 FROM marmut.artist WHERE email_akun = '{user_data.get('email')}'"
#     with connection.cursor() as cursor:
#         cursor.execute(query_artist)
#         user_data['is_artist'] = cursor.fetchone() is not None
    
#     #cek apakah dia songwriter atau tidak di table songwriter
#     query_songwriter = f"SELECT 1 FROM marmut.songwriter WHERE email_akun = '{user_data.get('email')}'"
#     with connection.cursor() as cursor:
#         cursor.execute(query_songwriter)
#         user_data['is_songwriter'] = cursor.fetchone() is not None

#     #cek apakah dia podcaster atau tidak di table podcaster
#     query_podcaster = f"SELECT 1 FROM marmut.podcaster WHERE email = '{user_data.get('email')}'"
#     with connection.cursor() as cursor:
#         cursor.execute(query_podcaster)
#         user_data['is_podcaster'] = cursor.fetchone() is not None
    
#     #cek apakah dia label atau tidak di table label
#     query_label = f"SELECT 1 FROM marmut.label WHERE email = '{user_data.get('email')}'"
#     with connection.cursor() as cursor:
#         cursor.execute(query_label)
#         user_data['is_label'] = cursor.fetchone() is not None
   
#     is_logged_in = True
#     user_data['is_logged_in'] = is_logged_in

#     # Query untuk mendapatkan informasi sesuai dengan role pengguna
#     query_info = ""
    
#     #kalau dia pengguna berarti yg penting dia ga label
#     print(user_data['is_label'])
#     if user_data['is_label'] == False:
#         print("masuk sini")
#         #status langganan pakai cek di html aja is_premium atau ga
#         query_info = f"""
        
#             SELECT nama, email, kota_asal, gender, tempat_lahir, tanggal_lahir
#             FROM marmut.akun
#             WHERE email = '{user_data.get('email')}'
#         """
#         with connection.cursor() as cursor:
#             cursor.execute(query_info)
#             columns = [col[0] for col in cursor.description]
#             user_info = dict(zip(columns, cursor.fetchone()))
#     elif user_data['is_label'] == True:
#         print("pipuppipip")
#         query_info = f"""
#             SELECT nama, email, kontak, kota_asal
#             FROM marmut.label
#             WHERE email = '{user_data.get('email')}'
#         """
#         with connection.cursor() as cursor:
#             cursor.execute(query_info)
#             columns = [col[0] for col in cursor.description]
#             user_info = dict(zip(columns, cursor.fetchone()))
#     # Tambahkan kondisi lain untuk role Artist, Songwriter, dan Podcaster jika diperlukan

   

#     # Query untuk mendapatkan playlist, lagu, podcast, atau album sesuai dengan role pengguna
#     playlists = []
#     songs_artist = []
#     songs_songwriter = []
#     podcasts = []
#     albums = []

#     # Contoh query untuk pengguna biasa
#     if user_data.get('is_label') == False:
#         query_playlists = f"""
#             SELECT judul
#             FROM marmut.user_playlist
#             WHERE email_pembuat = '{user_data.get('email')}'
#         """
#         with connection.cursor() as cursor:
#             cursor.execute(query_playlists)
#             playlists = [row[0] for row in cursor.fetchall()]
    
#     #kalau dia artist
#     if user_data.get('is_artist') == True :
#         #ambil dulu dari artist -> dpt id -> gabung sama song.id_artist =artist.id -> gabung sama konten.id = song.id_konten -> ambil judul
#         query_songs_artist = f"""
#             SELECT judul
#             FROM marmut.konten
#             JOIN marmut.artist ON song.id_artist = artist.id
#             JOIN marmut.song ON song.id_konten = konten.id
#             WHERE artist.email_akun = '{user_data.get('email')}'
#         """
#         with connection.cursor() as cursor:
#             cursor.execute(query_songs_artist)
#             songs_artist = [row[0] for row in cursor.fetchall()]

#        #kalau dia songwriter
#     if user_data.get('is_songwriter') == True:
#         query_songs_songwriter = f"""
#             SELECT judul
#             FROM marmut.konten
#             JOIN marmut.songwriter_write_song ON songwriter_write_song.id_song = konten.id
#             JOIN marmut.songwriter ON songwriter_write_song.id_songwriter = songwriter.id
#             WHERE songwriter.email_akun = '{user_data.get('email')}'
#         """
#         with connection.cursor() as cursor:
#             cursor.execute(query_songs_songwriter)
#             songs_songwriter = [row[0] for row in cursor.fetchall()]
#     #kalau dia podcaster
#     if user_data.get('is_podcaster') == True:
#         query_podcasts = f"""
#             SELECT nama_podcast
#             FROM marmut.podcast
#             WHERE host = '{user_data.get('email')}'
#         """
#         with connection.cursor() as cursor:
#             cursor.execute(query_podcasts)
#             podcasts = [row[0] for row in cursor.fetchall()]

#     #kalau dia label
#     if user_data.get('is_label') == True:
#         query_albums = f"""
#             SELECT nama_album
#             FROM marmut.album
#             WHERE label = '{user_data.get('email')}'
#         """
#         with connection.cursor() as cursor:
#             cursor.execute(query_albums)
#             albums = [row[0] for row in cursor.fetchall()]
#     #buat pass list roles
#     roles = []
#     if user_data.get('is_artist') == True:
#         roles.append('Artist')
#     if user_data.get('is_songwriter') == True:
#         roles.append('Songwriter')
#     if user_data.get('is_podcaster') == True:
#         roles.append('Podcaster')
#     if user_data.get('is_label') == True:
#         roles.append('Label')
#     if user_data.get('is_label') == False:
#         roles.append('Pengguna')
#     context = {
#         'user_data': user_info,
#         'role': ', '.join(roles),
#         'playlists': playlists,
#         'songs': songs,
#         'podcasts': podcasts,
#         'albums': albums
#     }

#     return render(request, 'dashboard.html', context)


# def dashboard(request):
#     # Ambil data pengguna dari session
#     user_data = request.session.get('user_data', {})
#     print(user_data)
#     # Query untuk mendapatkan informasi sesuai dengan role pengguna
#     query_info = ""
#     if user_data.get('role') == 'Pengguna':
#         query_info = f"""
#             SELECT nama, email, status_langganan, kota_asal, gender, tempat_lahir, tanggal_lahir, role
#             FROM marmut.akun
#             WHERE email = '{user_data.get('email')}'
#         """
#     elif user_data.get('role') == 'Label':
#         query_info = f"""
#             SELECT nama, email, kontak, kota_asal
#             FROM marmut.label
#             WHERE email = '{user_data.get('email')}'
#         """
#     # Tambahkan kondisi lain untuk role Artist, Songwriter, dan Podcaster jika diperlukan

#     with connection.cursor() as cursor:
#         cursor.execute(query_info)
#         columns = [col[0] for col in cursor.description]
#         user_info = dict(zip(columns, cursor.fetchone()))

#     # Query untuk mendapatkan playlist, lagu, podcast, atau album sesuai dengan role pengguna
#     playlists = []
#     songs = []
#     podcasts = []
#     albums = []

#     # Contoh query untuk pengguna
#     if user_data.get('role') == 'Pengguna':
#         query_playlists = f"""
#             SELECT nama_playlist
#             FROM playlist
#             WHERE pemilik = '{user_data.get('email')}'
#         """
#         cursor.execute(query_playlists)
#         playlists = [row[0] for row in cursor.fetchall()]

#     # Contoh query untuk Artist/Songwriter
#     if user_data.get('role') in ['Artist', 'Songwriter']:
#         query_songs = f"""
#             SELECT judul_lagu
#             FROM lagu
#             WHERE pemilik = '{user_data.get('email')}'
#         """
#         cursor.execute(query_songs)
#         songs = [row[0] for row in cursor.fetchall()]

#     # Contoh query untuk Podcaster
#     if user_data.get('role') == 'Podcaster':
#         query_podcasts = f"""
#             SELECT nama_podcast
#             FROM podcast
#             WHERE host = '{user_data.get('email')}'
#         """
#         cursor.execute(query_podcasts)
#         podcasts = [row[0] for row in cursor.fetchall()]

#     # Contoh query untuk Label
#     if user_data.get('role') == 'Label':
#         query_albums = f"""
#             SELECT nama_album
#             FROM album
#             WHERE label = '{user_data.get('email')}'
#         """
#         cursor.execute(query_albums)
#         albums = [row[0] for row in cursor.fetchall()]

#     context = {
#         'user_data': user_info,
#         'playlists': playlists,
#         'songs': songs,
#         'podcasts': podcasts,
#         'albums': albums
#     }

#     return render(request, 'dashboard.html', context)
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
                    #request.session['is_logged_in'] = True
                    print("hihi")
                    print(request.session['user_data'])
                    return redirect('akun:dashboard')
                else:
                    messages.error(request, 'Maaf, password yang Anda masukkan salah.')
            else:
                messages.error(request, 'Pengguna tidak ditemukan.')

    return render(request, "login.html")



# @csrf_exempt
# def login_with_postgres(request):
#     is_premium = False
#     is_artist = False
#     is_songwriter = False 
#     is_podcaster = False
#     is_label = False
#     is_logged_in = False

#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
        
#         # Query untuk mencari pengguna berdasarkan email di tabel akun
#         query_akun = f"""
#             SELECT * FROM marmut.akun WHERE email = '{email}'
#         """

#         with connection.cursor() as cursor:
#             cursor.execute(query_akun)
#             columns = [col[0] for col in cursor.description]
#             matching_users_akun = [dict(zip(columns, row)) for row in cursor.fetchall()]

#         if matching_users_akun:
#             user_akun = matching_users_akun[0]



#              # Check for artist
#             query_artist = f"SELECT 1 FROM marmut.artist WHERE email_akun = '{email}'"
#             with connection.cursor() as cursor:
#                     cursor.execute(query_artist)
#                     is_artist = cursor.fetchone() is not None

#                 # Check for songwriter
#             query_songwriter = f"SELECT 1 FROM marmut.songwriter WHERE email_akun = '{email}'"
#             with connection.cursor() as cursor:
#                     cursor.execute(query_songwriter)
#                     is_songwriter = cursor.fetchone() is not None

#                 # Check for podcaster
#             query_podcaster = f"SELECT 1 FROM marmut.podcaster WHERE email = '{email}'"
#             with connection.cursor() as cursor:
#                     cursor.execute(query_podcaster)
#                     is_podcaster = cursor.fetchone() is not None

#                 # Check for label
#             query_label = f"SELECT 1 FROM marmut.label WHERE email = '{email}'"
#             with connection.cursor() as cursor:
#                     cursor.execute(query_label)
#                     is_label = cursor.fetchone() is not None
#             if user_akun['password'] == password:
#                 # Set user data in session
#                 is_logged_in = True
#                 request.session['user_data'] = {
#                     'email': user_akun['email'],
#                     'nama': user_akun.get('nama', ''),  
#                     'password': password,
#                     'is_premium': is_premium,
#                     'is_artist': is_artist,
#                     'is_songwriter': is_songwriter,
#                     'is_podcaster': is_podcaster,
#                     'is_label': is_label,
#                     'is_logged_in': is_logged_in
#                 }
#                 print("aaaaaaa")
#                 print(is_songwriter)
#                 print(is_logged_in)
                
#                 return render(request, 'dashboard.html')
#             else:
#                 messages.error(request, 'Maaf, password yang Anda masukkan salah.')
#         else:
#             messages.error(request, 'Pengguna tidak ditemukan.')

#     return render(request, "login.html")


#BATASSSSSSSSSSSSSSSSS
#syarat untuk login unik akunnya 
# @csrf_exempt
# def login_with_postgres(request):
#     is_premium = False
#     is_artist = False
#     is_songwriter = False 
#     is_podcaster = False
#     is_label = False

#     matching_users_akun = 0

#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
        
#         # Query untuk mencari pengguna berdasarkan email di tabel akun
#         query_akun = f"""
#             SELECT *,
#                 CASE WHEN EXISTS (
#                     SELECT 1 FROM marmut.akun u
#                     WHERE u.email = '{email}'
#                 ) THEN 'true'
#                 ELSE 'false' END AS is_user
#             FROM marmut.akun WHERE email = '{email}'
#         """

#         #cursor.execute
#         with connection.cursor() as cursor:
#             cursor.execute(query_akun)
#             matching_users_akun = cursor.fetchall()
        
#         if matching_users_akun :
#               return render(request, "dashboard.html")

#         #matching_users_akun kalau ada 
#         # print("match: " +  matching_users_akun)
#         #batas batas
#         # if len(matching_users_akun) == 0 and len(matching_users_label) == 0:
#         #     # Jika email tidak ditemukan di kedua tabel
#         #     messages.error(request, 'Pengguna tidak ditemukan.')
#         # else:
#         #     # Jika email ditemukan di salah satu atau kedua tabel
#         #     user_data = {}
            
#         #     if len(matching_users_akun) > 0:
#         #         # Jika pengguna ada di tabel akun
#         #         user_akun = matching_users_akun[0]
#         #         if user_akun['password'] == password:
#         #             # Jika password sesuai, ambil informasi pengguna dari tabel akun
#         #             user_data['email'] = user_akun['email']
#         #             user_data['nama'] = user_akun['nama']
#         #             user_data['kota_asal'] = user_akun['kota_asal']
#         #             user_data['gender'] = user_akun['gender']
#         #             user_data['tempat_lahir'] = user_akun['tempat_lahir']
#         #             user_data['tanggal_lahir'] = user_akun['tanggal_lahir']
                    

#         #             roles = []
#         #             # Cek role pengguna
#         #              # Cek apakah email pengguna ada di tabel Premium
#         #             query_premium = f"""
#         #                 SELECT * FROM marmut.premium
#         #                 WHERE email = '{user_akun['email']}'
#         #             """
#         #             matching_premium = execute_sql_query(query=query_premium)
#         #             if len(matching_premium) > 0:
#         #                 roles.append('Premium')
#         #                 is_premium = True
                    
#         #             # Cek apakah email pengguna ada di tabel Artist
#         #             query_artist = f"""
#         #                 SELECT * FROM marmut.artist
#         #                 WHERE email = '{user_akun['email']}'
#         #             """
#         #             matching_artist = execute_sql_query(query=query_artist)
#         #             if len(matching_artist) > 0:
#         #                 roles.append('Artist')
#         #                 is_artist = True
                    
#         #             # Cek apakah email pengguna ada di tabel Songwriter
#         #             query_songwriter = f"""
#         #                 SELECT * FROM marmut.songwriter
#         #                 WHERE email = '{user_akun['email']}'
#         #             """
#         #             matching_songwriter = execute_sql_query(query=query_songwriter)
#         #             if len(matching_songwriter) > 0:
#         #                 roles.append('Songwriter')
#         #                 is_songwriter = True
                    
#         #             # Cek apakah email pengguna ada di tabel Podcaster
#         #             query_podcaster = f"""
#         #                 SELECT * FROM marmut.podcaster
#         #                 WHERE email = '{user_akun['email']}'
#         #             """
#         #             matching_podcaster = execute_sql_query(query=query_podcaster)
#         #             if len(matching_podcaster) > 0:
#         #                 roles.append('Podcaster')
#         #                 is_podcaster = True
                    
                    
#         #             user_data['role'] = ', '.join(roles)
#         #             #berarti pengguna biasa ga ada is_pengguna biasa tapi cek aja is dari tiap role
#         #             request.session['user_data'] = {
#         #                 'email': email,
#         #                 'nama': user_akun.get('nama', ''),  
#         #                 'password': password,
#         #                 'is_premium' : is_premium,
#         #                 'is_artist' : is_artist,
#         #                 'is_songwriter' : is_songwriter ,
#         #                 'is_podcaster' : is_podcaster,
#         #                 'is_label' : is_label
#         #             }
                    
#         #             # Redirect ke halaman dashboard pengguna
#         #             return HttpResponseRedirect('/dashboard/')
#         #         else:
#         #             messages.error(request, 'Maaf, password yang Anda masukkan salah.')
            
#         #     if len(matching_users_label) > 0:
#         #         # Jika pengguna ada di tabel label
#         #         user_label = matching_users_label[0]
#         #         # Ambil informasi pengguna dari tabel label
#         #         if user_label['password'] == password:
#         #             user_data['email'] = user_label['email']
#         #             user_data['nama'] = user_label['nama']
#         #             user_data['kontak'] = user_label['kontak']


#         #             # request.session['user_data'] = {
#         #             #     'email': email,
#         #             #     'nama': user_akun.get('nama', ''),  
#         #             #     'password': password
#         #             # }

#         #             request.session['user_data'] = {
#         #                 'email': email,
#         #                 'nama': user_akun.get('nama', ''),  
#         #                 'password': password,
#         #                 'is_premium' : is_premium,
#         #                 'is_artist' : is_artist,
#         #                 'is_songwriter' : is_songwriter ,
#         #                 'is_podcaster' : is_podcaster,
#         #                 'is_label' : is_label
#         #             }

#         #             #next -> blm tambahin di views(?)
#         #             return HttpResponseRedirect('label/label_dashboard/')
#         #         else: 
#         #             messages.error(request, 'Maaf, password yang Anda masukkan salah.')
#         #         #next : ini bisa ditaruh di views.py untuk di app label aja -> buat nampilin semua album yang dimiliki oleh label teresebut 
#         #         # # Query untuk mencari album milik label
#         #         # query_album = f"""
#         #         #     SELECT * FROM marmut.album
#         #         #     WHERE id_label = '{user_label['id']}'
#         #         # """
#         #         # # Eksekusi query album
#         #         # # matching_albums = execute_sql_query(query=query_album)
#         #         # if len(matching_albums) == 0:
#         #         #     messages.info(request, 'Belum Memproduksi Album')
                
#         #         # Redirect ke halaman dashboard label
                   
                
#     return render(request, "login.html")
#BATASSSSSSSSSSSSSS

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

        return redirect('login')  # Ubah 'login' sesuai dengan nama URL untuk halaman login

    return render(request, 'register_label.html')

#register pengguna 
@csrf_exempt
#TO DO: apakah sebenarnya pas insert itu boleh null, kalau begitu insert seperti biasa saja NEXT 
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
            
            return HttpResponseRedirect('/login/') 
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
# def logout_view(request):
#     # Hapus data sesi
#     request.session.flush()

#     # Redirect ke halaman login
#     return redirect('akun:login')