from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
# from .forms import LoginForm -> ga usah pakai form langsung dari login.html aja(?)
import json
from django.db import connection
from connect_postgres import execute_sql_query
from django.shortcuts import render, redirect
from django.http import JsonResponse,HttpResponseRedirect
import datetime
import uuid
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.urls import reverse
import psycopg2

def show_home(request):
    return render(request, "home.html")

def show_register(request):
    return render(request, "register.html")

def show_login(request):
    return render(request, "login.html")
#next blm ganti


@csrf_exempt
def logout_with_postgres(request):
    # Hapus data sesi pengguna
    if 'user_data' in request.session:
        del request.session['user_data']
    
    # Lakukan logout pengguna menggunakan fungsi bawaan Django
    
    # Redirect ke halaman login atau halaman lain yang sesuai
    return redirect('home')  #based dari nama yang dibentuk di urls.py

@csrf_exempt
def register_with_postgres(request):
    if request.method == 'POST':
        # SAMA ---------------------------
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        phone_num = request.POST.get('phone_num')
        # SAMA -------------------------------------
        # HANYA CUSTOMER ---------------------------
        nik = request.POST.get('nik')
        # HANYA HOTEL ------------------------------
        hotel_name = request.POST.get('hotel_name')
        hotel_branch = request.POST.get('hotel_branch')
        nib = request.POST.get('nib')
        star = request.POST.get('star')
        street = request.POST.get('street')
        district = request.POST.get('district')
        city = request.POST.get('city')
        province = request.POST.get('province')
        description = request.POST.get('description')
        min_checkout = request.POST.get('min_checkout')
        max_checkout = request.POST.get('max_checkout')
        print(hotel_name)

        # CEK REGISTER CUSTOMER ATAU HOTEL
        is_customer = True if nik is not None else False

        # CEK CUSTOMER
        if is_customer and not all([email.strip(), password.strip(), confirm_password.strip(), fname.strip(), lname.strip(), nik.strip(), phone_num.strip()]):
            messages.error(request, 'Mohon lengkapi field yang kosong dalam mendaftarkan customer.')
        # CEK HOTEL
        elif not is_customer and not all([email.strip(), password.strip(),
         confirm_password.strip(), fname.strip(), lname.strip(), 
           hotel_name.strip(), hotel_branch.strip(), nib.strip(), star, 
           street.strip(),district.strip(),city.strip(), 
           province.strip(), description.strip(),  
           min_checkout.strip(), max_checkout.strip(), phone_num.strip()]):
            messages.error(request, 'Mohon lengkapi field yang kosong dalam mendaftarkan hotel.')
        # CEK BINTANG
        elif not is_customer and not star.isdigit():
            messages.error(request, 'Maaf, bintang hotel harus bilangan bulat.')
        # CEK RANGE BINTANG
        elif not is_customer and (float(star) < 1 or float(star) > 5):
            messages.error(request, 'Maaf, bintang hotel harus ada di range 1 sampai 5.')
        # CEK PASSWORD
        elif password != confirm_password:
            messages.error(request, 'Password dan konfirmasi password tidak cocok.')
        else:
            if is_customer:
                query= f"""

                INSERT INTO sistel.user  (email, password, fname, lname) VALUES ('{email}','{password}', '{fname}', '{lname}');
                INSERT INTO reservation_actor (email, phonenum) VALUES ('{email}','{phone_num}');
                INSERT INTO customer  (email, nik) VALUES ('{email}','{nik}')
                RETURNING email;
                
                """
            else:
                query = f"""
                INSERT INTO sistel.user  (email, password, fname, lname) VALUES ('{email}','{password}', '{fname}', '{lname}');
                INSERT INTO reservation_actor (email, phonenum) VALUES ('{email}','{phone_num}');
                INSERT INTO hotel 
                (email, hotel_name, hotel_branch, nib, star, street, district, city,
                  province, description, max_checkout, min_checkout) VALUES (
                    '{email}', '{hotel_name}', '{hotel_branch}', '{nib}',
                      {star}, '{street}', '{district}', '{city}', '{province}',
                        '{description}', '{max_checkout}', '{min_checkout}'
                  )
                RETURNING email;

                """
            try:
                execute_sql_query(query=query)
                return HttpResponseRedirect('/login/') 
            except psycopg2.Error as error:
                messages.error(request, f'{error}')
            except Exception as error:
                messages.error(request, f'{error}')
    return render(request,"register.html")


         
#LOGINNNNNNNNNNN       
        #  ketika masuk pertama kali berarti -> ada dua kemungkinan bisa label atau bisa saja pengguna . 
        #     ketika masuk sebagai pengguna maka ada kombinasi dair 3 kemungkiann -> bisa podcaster artsit atau songwriter 
        #     nah ini caranya denagn loop ke semua table terkait saja lalu                    pakekkan is untuk setiap 


        #     is_user -> kalau dia ada di akun 
        #     is_premium
        #     is_artist
        #     is_songwriter
        #     is_podcaster
        #     is_label

        #cek dulu apakah emailnya ada di akun (is_user jadi true kalau ada ) atau ada di table label (is_label jadi true kalau ada )
        # kalau misalnya ada ga ada di keduanya maka berikan mesage error pengguna tidak ditemukan.

        #kalau email ditemukan entah salah satu di table akun atau di table label
        #maka cek apakah passwordnya benar -> kalau passwordnya benar
        #kalau passwordnya salah berikan pesan error bahwa password salah 
        #kalau passwordnya benar lalu selanjutnya akan ke dashboard.html tetapi sebelumnya skenarionya speerti ini  
        

        #sekanrionya pasti salah satu entah is_user true atau is_label yang true
        #kalau is_user true, ambil nama, email, kota asal, gender, tempat lahir, tanggal lahir yang dipunya user 
        #ini kayaknya ga ada hubungan dulu ke user premium atau ga -> tapi yg penting megang email bisa disearch dia premium atau ga 
        #nah ada role -> ini ntar diisi dengan is aja , kalau cmn is_user saja yg true maka jadi pengguna biasa, kalau yang lainnya ada
        #is_podcaster gtgt masuk  berarti nanti tinggal ditambhin aja di rolenya saja-> di kode htmlnya saja. (pakai if)
        
        #kalau dia is_user nya true dan is_labelnya false, maka unutk isi tiap kemungkinan is 
        #kita cek apakah email user tersebut ada atau tidak di table artist, table songwriter, dan  tabel podcaster


        #kalau dia is_user false dan is_label true -> maka kita ambil nama, email, kontak, dan 
        #dan dari ambil id_label nya buat nanti mencari semua album yang id_label sama dengan label.id dari user yang log in  ini. 
        #dan nanti di htmlnya ada menampilkan kode untuk nampilin album id ini -> next atau hmm buat views baru aja 
        #kalau ternyata id labelnya tidak ada di table album maka tampilan pesan nanti di htmlnya belum memproduksi album 

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
            SELECT *,
                CASE WHEN EXISTS (
                    SELECT 1 FROM marmut.akun u
                    WHERE u.email = '{email}'
                ) THEN 'true'
                ELSE 'false' END AS is_user
            FROM marmut.akun WHERE email = '{email}'
        """
        # Eksekusi query tabel akun
        matching_users_akun = execute_sql_query(query=query_akun)
        
        # Query untuk mencari pengguna berdasarkan email di tabel label
        query_label = f"""
            SELECT *,
                CASE WHEN EXISTS (
                    SELECT 1 FROM marmut.label l
                    WHERE l.email = '{email}'
                ) THEN 'true'
                ELSE 'false' END AS is_label
            FROM marmut.label WHERE email = '{email}'
        """
        # Eksekusi query tabel label
        matching_users_label = execute_sql_query(query=query_label)
        
        if len(matching_users_akun) == 0 and len(matching_users_label) == 0:
            # Jika email tidak ditemukan di kedua tabel
            messages.error(request, 'Pengguna tidak ditemukan.')
        else:
            # Jika email ditemukan di salah satu atau kedua tabel
            user_data = {}
            
            if len(matching_users_akun) > 0:
                # Jika pengguna ada di tabel akun
                user_akun = matching_users_akun[0]
                if user_akun['password'] == password:
                    # Jika password sesuai, ambil informasi pengguna dari tabel akun
                    user_data['email'] = user_akun['email']
                    user_data['nama'] = user_akun['nama']
                    user_data['kota_asal'] = user_akun['kota_asal']
                    user_data['gender'] = user_akun['gender']
                    user_data['tempat_lahir'] = user_akun['tempat_lahir']
                    user_data['tanggal_lahir'] = user_akun['tanggal_lahir']
                    

                    roles = []
                    # Cek role pengguna
                     # Cek apakah email pengguna ada di tabel Premium
                    query_premium = f"""
                        SELECT * FROM marmut.premium
                        WHERE email = '{user_akun['email']}'
                    """
                    matching_premium = execute_sql_query(query=query_premium)
                    if len(matching_premium) > 0:
                        roles.append('Premium')
                        is_premium = True
                    
                    # Cek apakah email pengguna ada di tabel Artist
                    query_artist = f"""
                        SELECT * FROM marmut.artist
                        WHERE email = '{user_akun['email']}'
                    """
                    matching_artist = execute_sql_query(query=query_artist)
                    if len(matching_artist) > 0:
                        roles.append('Artist')
                        is_artist = True
                    
                    # Cek apakah email pengguna ada di tabel Songwriter
                    query_songwriter = f"""
                        SELECT * FROM marmut.songwriter
                        WHERE email = '{user_akun['email']}'
                    """
                    matching_songwriter = execute_sql_query(query=query_songwriter)
                    if len(matching_songwriter) > 0:
                        roles.append('Songwriter')
                        is_songwriter = True
                    
                    # Cek apakah email pengguna ada di tabel Podcaster
                    query_podcaster = f"""
                        SELECT * FROM marmut.podcaster
                        WHERE email = '{user_akun['email']}'
                    """
                    matching_podcaster = execute_sql_query(query=query_podcaster)
                    if len(matching_podcaster) > 0:
                        roles.append('Podcaster')
                        is_podcaster = True
                    
                    
                    user_data['role'] = ', '.join(roles)
                    #berarti pengguna biasa ga ada is_pengguna biasa tapi cek aja is dari tiap role
                    request.session['user_data'] = {
                        'email': email,
                        'nama': user_akun.get('nama', ''),  
                        'password': password,
                        'is_premium' : is_premium,
                        'is_artist' : is_artist,
                        'is_songwriter' : is_songwriter ,
                        'is_podcaster' : is_podcaster,
                        'is_label' : is_label
                    }
                    
                    # Redirect ke halaman dashboard pengguna
                    return HttpResponseRedirect('/dashboard/')
                else:
                    messages.error(request, 'Maaf, password yang Anda masukkan salah.')
            
            if len(matching_users_label) > 0:
                # Jika pengguna ada di tabel label
                user_label = matching_users_label[0]
                # Ambil informasi pengguna dari tabel label
                if user_label['password'] == password:
                    user_data['email'] = user_label['email']
                    user_data['nama'] = user_label['nama']
                    user_data['kontak'] = user_label['kontak']


                    # request.session['user_data'] = {
                    #     'email': email,
                    #     'nama': user_akun.get('nama', ''),  
                    #     'password': password
                    # }

                    request.session['user_data'] = {
                        'email': email,
                        'nama': user_akun.get('nama', ''),  
                        'password': password,
                        'is_premium' : is_premium,
                        'is_artist' : is_artist,
                        'is_songwriter' : is_songwriter ,
                        'is_podcaster' : is_podcaster,
                        'is_label' : is_label
                    }

                    #next -> blm tambahin di views(?)
                    return HttpResponseRedirect('label/label_dashboard/')
                else: 
                    messages.error(request, 'Maaf, password yang Anda masukkan salah.')
                #next : ini bisa ditaruh di views.py untuk di app label aja -> buat nampilin semua album yang dimiliki oleh label teresebut 
                # # Query untuk mencari album milik label
                # query_album = f"""
                #     SELECT * FROM marmut.album
                #     WHERE id_label = '{user_label['id']}'
                # """
                # # Eksekusi query album
                # # matching_albums = execute_sql_query(query=query_album)
                # if len(matching_albums) == 0:
                #     messages.info(request, 'Belum Memproduksi Album')
                
                # Redirect ke halaman dashboard label
                   
                
    return render(request, "login.html")

#khusus pengguna 
#next cek dulu ini bener atau ga
@csrf_exempt
def dashboard_view(request):
    user_data = request.session.get('user_data')
    if not user_data:
        messages.error(request, 'Anda harus login terlebih dahulu.')
        return render(request, 'login.html')

    playlists = []
    songs = []
    podcasts = []

    if not user_data.get('is_artist') and not user_data.get('is_podcaster') and not user_data.get('is_songwriter'):
        # Jika pengguna bukan artist, podcaster, atau songwriter, maka cari playlistnya
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM marmut.user_playlist WHERE email_pembuat = %s", [user_data['email']])
            playlists = cursor.fetchall()
        
    if user_data.get('is_artist') or user_data.get('is_songwriter'):
        # Jika pengguna adalah artist atau songwriter, maka cari lagu yang dimilikinya
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM marmut.song WHERE id_artist = %s", [user_data['email']])
            songs = cursor.fetchall()
        
    if user_data.get('is_podcaster'):
        # Jika pengguna adalah podcaster, maka cari podcast yang dimilikinya
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM marmut.podcast WHERE email_podcaster = %s", [user_data['email']])
            podcasts = cursor.fetchall()

    context = {
        'user_data': user_data,
        'playlists': playlists,
        'songs': songs,
        'podcasts': podcasts,
    }

    return render(request, 'dashboard.html', context)
# @csrf_exempt
# def login_with_postgres(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         query = f"""
#     SELECT *,
#         CASE WHEN EXISTS (
#             SELECT 1 FROM sistel.user u
#             INNER JOIN hotel ON u.email = hotel.email
#             WHERE u.email = '{email}'
#         ) THEN 'false'
#         ELSE 'true' END AS is_pengguna
#     FROM sistel.user WHERE email = '{email}'
#     """
#         matching_users = execute_sql_query(query=query)
        
#        # print(matching_users)
#         if len(matching_users) == 0:
#             messages.error(request, 'Pengguna tidak ditemukan.')
#         else:
#           #  print(matching_users)
#             selected_user = matching_users[0]
#             user_store_password = selected_user[1]
#             user_fname = selected_user[2]
#             user_lname = selected_user[3]
#             is_user = selected_user[4]
#             if user_store_password == password:
#                 request.session['user_data'] = {
#                     'email': email,
#                     'fname': user_fname,
#                     'lname': user_lname,
#                     'is_hotel': is_user == 'false'
#                 }
#                 print(request.session['user_data'])
#                 # TODO: ganti redirect ke dashboard
#                 if is_user == 'false':
#                     return HttpResponseRedirect('/hotel/dashboard/') 
#                 return HttpResponseRedirect('/reservasi/dashboard/')  
#             messages.error(request, 'Maaf, password yang kamu masukkan salah.')
#     return render(request,"login.html")


# def login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 # Redirect ke halaman Dashboard sesuai peran pengguna
#                 if user.is_artist:
#                     return redirect('artist_dashboard')
#                 elif user.is_songwriter:
#                     return redirect('songwriter_dashboard')
#                 elif user.is_podcaster:
#                     return redirect('podcaster_dashboard')
#                 else:
#                     return redirect('user_dashboard')
#             else:
#                 messages.error(request, 'Email atau password salah.')
#     else:
#         form = LoginForm()
#     return render(request, 'login.html', {'form': form})
