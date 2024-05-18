from datetime import timedelta
from pyexpat.errors import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
import psycopg2
from django.db import connection

# Create your views here.
def show_langganan_paket(request):
    user_data = request.session.get('user_data', {})

    query = """
    set search_path to marmut;
    select * from paket
    """
    
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

    print("\n================ DEBUG AREA ================")
    for key, value in user_data.items():
        print(f"{key}: {value}")
    print("================ DEBUG AREA ================\n")

    paket = {
        result[0][0]: result[0][1],
        result[1][0]: result[1][1],
        result[2][0]: result[2][1],
        result[3][0]: result[3][1]
    }

    context = {
        'paket': paket
    }
    return render(request, "langganan_paket.html", context)

def show_finalisasi_paket(request, jenis, harga):
    context = {
        'jenis_paket': jenis,
        'harga_paket': harga
    }
    return render(request, "finalisasi_langganan.html", context)

def beli_paket(request):
    print("INI METHODNYA: " + request.method)
    if request.method == 'POST':
        user_data = request.session.get('user_data', {})
        email = user_data.get('email')
        jenis_paket = request.POST.get('jenis_paket')
        metode_bayar = request.POST.get('metode_bayar')
        harga_paket = int(request.POST.get('harga_paket'))
        timestamp_dimulai = timezone.now()
        if (jenis_paket == "1 bulan"):
            timestamp_berakhir = timestamp_dimulai + timedelta(days=30)
        elif (jenis_paket == "2 bulan"):
            timestamp_berakhir = timestamp_dimulai + timedelta(days=60)
        elif (jenis_paket == "6 bulan"):
            timestamp_berakhir = timestamp_dimulai + timedelta(days=180)
        else:
            timestamp_berakhir = timestamp_dimulai + timedelta(days=365)

        print(email)
        print(jenis_paket)
        print(metode_bayar)
        print(harga_paket)
        print(timestamp_dimulai)
        print(timestamp_berakhir)

        if not email or not jenis_paket or not metode_bayar or not harga_paket:
            return JsonResponse({'error': 'Data tidak lengkap'}, status=400)

        insert_query = """
        SET search_path TO marmut;
        INSERT INTO TRANSACTION (id, jenis_paket, email, timestamp_dimulai, timestamp_berakhir, metode_bayar, nominal)
        VALUES (gen_random_uuid(), %s, %s, %s, %s, %s, %s);
        """

        try:
            with connection.cursor() as cursor:
                cursor.execute(insert_query, [jenis_paket, email, timestamp_dimulai, timestamp_berakhir, metode_bayar, harga_paket])

            # Tambahkan entri di tabel PREMIUM
            insert_premium_query = """
            INSERT INTO PREMIUM (email) VALUES (%s)
            ON CONFLICT (email) DO NOTHING;
            """
            with connection.cursor() as cursor:
                cursor.execute(insert_premium_query, [email])
                cursor.execute("DELETE FROM marmut.nonpremium WHERE email = %s", (email,))
            user_data["is_premium"] = True

            print("\n================ DEBUG AREA ================")
            for key, value in user_data.items():
                print(f"{key}: {value}")
            print("================ DEBUG AREA ================\n")

            return JsonResponse({'success': 'Paket langganan berhasil dibeli'}, status=200)
        
        except (Exception, psycopg2.DatabaseError) as error:
            print("\n================ DEBUG AREA ================")
            for key, value in user_data.items():
                print(f"{key}: {value}")
            print("================ DEBUG AREA ================\n")
            return JsonResponse({'error': str(error)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def show_riwayat_langganan(request):
    user_data = request.session.get('user_data', {})
    email = user_data['email']

    query = """
    SELECT jenis_paket, TO_CHAR(timestamp_dimulai, 'DD Month YYYY, HH24:MI'),
    TO_CHAR(timestamp_berakhir, 'DD Month YYYY, HH24:MI'), metode_bayar, 
    TO_CHAR(nominal, '999,999')
    FROM marmut.transaction
    WHERE email = %s;
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (email,))
        riwayat_transaksi = cursor.fetchall()
        print(riwayat_transaksi)

    context = {
        'riwayat_transaksi': riwayat_transaksi
    }

    return render(request, "riwayat_langganan.html", context)