from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
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

@login_required
def dashboard(request):
    # Anda bisa menambahkan logika di sini untuk mengambil data yang diperlukan untuk dashboard
    #next ini bisa ditambahkan logika apa role dari pengguna tersebut , atau mungkin bisa di dahsbroad htmlnya sendiri kita pakai untuk variabel yang ada. 
    return render(request, 'dashboard.html')

#loginnn



@csrf_exempt
def login_with_postgres(request):
    is_premium = False
    is_artist = False
    is_songwriter = False 
    is_podcaster = False
    is_label = False

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Query untuk mencari pengguna berdasarkan email di tabel akun
        query_akun = f"""
            SELECT * FROM marmut.akun WHERE email = '{email}'
        """

        with connection.cursor() as cursor:
            cursor.execute(query_akun)
            columns = [col[0] for col in cursor.description]
            matching_users_akun = [dict(zip(columns, row)) for row in cursor.fetchall()]

        if matching_users_akun:
            user_akun = matching_users_akun[0]
            if user_akun['password'] == password:
                # Set user data in session
                request.session['user_data'] = {
                    'email': user_akun['email'],
                    'nama': user_akun.get('nama', ''),  
                    'password': password,
                    'is_premium': is_premium,
                    'is_artist': is_artist,
                    'is_songwriter': is_songwriter,
                    'is_podcaster': is_podcaster,
                    'is_label': is_label
                }
                return render(request, 'dashboard.html')
            else:
                messages.error(request, 'Maaf, password yang Anda masukkan salah.')
        else:
            messages.error(request, 'Pengguna tidak ditemukan.')

    return render(request, "login.html")


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
def register_pengguna(request):
    if request.method == 'POST':
        # SAMA ---------------------------
        email = request.POST.get('email')
        password = request.POST.get('password')
        nama = request.POST.get('nama')
        gender = request.POST.get('gender')
        tempat_lahir = request.POST.get('tempat_lahir')
        tanggal_lahir = request.POST.get('tanggal_lahir')
        kota_asal = request.POST.get('kota_asal')
        roles = request.POST.getlist('role')
        is_verified = True

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
       
            
        
            return HttpResponseRedirect('/login/') 
            # except psycopg2.Error as error:
            #     messages.error(request, f'{error}')
            # except Exception as error:
            #     messages.error(request, f'{error}')
    return render(request, 'register_pengguna.html')
