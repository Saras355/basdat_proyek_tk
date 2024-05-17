
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
        
        
      
        #carik di artist_id pakai query dah 
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM marmut.artist WHERE email_akun = %s", [artists])
            artist_id = cursor.fetchone()[0]
        
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
            cursor.execute("INSERT INTO marmut.album (id, judul, jumlah_lagu, id_label, total_durasi) VALUES (%s, %s, %s, %s, %s)", [album_id, judul_album, 1, label_id, int(durasi)])
            cursor.execute("INSERT INTO marmut.song (id_konten, id_artist, id_album) VALUES (%s, %s, %s)", [song_id, artist_id, album_id])
            for genre_id in genre_masuk:
                cursor.execute("INSERT INTO marmut.genre (id_konten, genre) VALUES (%s, %s)", [song_id, genre_id])
            for songwriter_id in songwriter_ids:
                cursor.execute("INSERT INTO marmut.songwriter_write_song (id_songwriter, id_song) VALUES (%s, %s)", [songwriter_id, song_id])


        #NEXT HABIS INI KAYAKNYA AMBIL SEMUA SYANG BISA PUNYA ROYALTI DAH SEPERTI ARTIST, LABEL, SONGWRITER 
        # TAPI MASALAHNYA RIYALTI NYA GA TAU BERAPAAN
        return HttpResponse(f'Album {judul_album} berhasil dibuat dengan artist: {label_str}{(artists)}, songwriters: {", ".join(songwriters)}, genres: {", ".join(genres)}, durasi: {durasi} menit.')
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
        