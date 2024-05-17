from django.shortcuts import render

# Create your views here.
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


#membuat untuk views dashboard terlebih dahulu 
@login_required
def dashboard(request):
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

                print("\n================ DEBUG AREA ================")
                print(request.session)
                for key, value in request.session['user_data'].items():
                    print(f"{key}: {value}")
                print("\n")
                print(user_akun['email'])
                # cek_premium(user_akun['email'])
                print("================ DEBUG AREA ================\n")
                
                return render(request, 'dashboard.html')
            else:
                messages.error(request, 'Maaf, password yang Anda masukkan salah.')
        else:
            messages.error(request, 'Pengguna tidak ditemukan.')

    return render(request, "login.html")

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
       
            
        
            return HttpResponseRedirect('login/') 
            # except psycopg2.Error as error:
            #     messages.error(request, f'{error}')
            # except Exception as error:
            #     messages.error(request, f'{error}')
    return render(request, 'register_pengguna.html')

def cek_premium(email):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SET search_path TO marmut;
            SELECT * FROM nonpremium WHERE email = %s;
            """,
            (email,)
        )
        res = cursor.fetchall()
    print(res)
