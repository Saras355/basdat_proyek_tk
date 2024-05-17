def create_album(request):
    user_data = request.session.get('user_data', {})
    is_artist = user_data.get('is_artist', False)
    is_songwriter = user_data.get('is_songwriter', False)
    user_id = user_data.get('user_id', None)
    email = user_data.get('email', None)

    print("test userdata")
    print(user_data)
    if not (is_artist or is_songwriter):
        return HttpResponse("You are not authorized to access this page", status=403)

    if request.method == "POST":
        print("Semua data dalam request.POST:")
        for a in request.POST:
            print(a)
        judul_album = request.POST.get('judul_album')
        print(judul_album)
        label_id = request.POST.get('label')
        print("label iddddddddddd")
        print(label_id)
        album_id = str(uuid.uuid4())
        artists = request.POST.getlist('artist[]')
        print("kasik artist")
        

        #untuk section lagu pertama
        judul_lagu = request.POST['judul_lagu']
        artist_id = request.POST.get('artist')        
      
        songwriter_ids = request.POST.getlist('songwriter.id')
        print(songwriter_ids)
        genre_ids = request.POST.getlist('genre.id')
        durasi = request.POST['durasi']
        song_id = str(uuid.uuid4())
        print(song_id)
        tanggal_rilis = datetime.datetime.now()
        tahun = tanggal_rilis.year
        print(album_id)

        #insert ke table konteen dulu
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO marmut.konten (id, judul,  tanggal_rilis, tahun, durasi) VALUES (%s, %s, %s, %s, %s)", [song_id, judul_lagu, tanggal_rilis, tahun, durasi])
            #cursor.execute("INSERT INTO marmut.artist (artist_id, song_id) VALUES (%s, %s)", [artist_id, song_id])
         #masukkan ke album
            cursor.execute("INSERT INTO marmut.album (id, judul, jumlah_lagu, id_label, total_durasi) VALUES (%s, %s, %s, %s, %s)", [album_id, judul_album, 1, label_id, int(durasi)])
        
        with connection.cursor() as cursor:
            #ke table song -> artistnya pasti satu
            cursor.execute("INSERT INTO marmut.song (id_konten, id_artist, id_album) VALUES (%s, %s, %s)", [song_id, artist_id, album_id])

            for genre_id in genre_ids:
                cursor.execute("INSERT INTO marmut.genre (id_konten, genre) VALUES (%s, %s)", [song_id, genre_id])
            #ini ga perlu karena dia sudah ada di table songwriter
            # for songwriter_id in songwriter_ids:
            #     cursor.execute("INSERT INTO marmut.songwriter_writes_song (songwriter_id, song_id) VALUES (%s, %s)", [songwriter_id, song_id])

            #songwriter_write_song
            for songwriter_id in songwriter_ids:
                cursor.execute("INSERT INTO marmut.songwriter_write_song (id_songwriter, id_song) VALUES (%s, %s)", [songwriter_id, song_id])


           
        # #insert into table song dulu -> biarin album id null dulu, ntar diupdate
        # with connection.cursor() as cursor:
        #     cursor.execute("INSERT INTO marmut.song (id_konten, id_artist) VALUES (%s, %s, %s)", [song_id, judul_lagu, durasi])
        #     for songwriter_id in songwriter_ids:
        #         cursor.execute("INSERT INTO marmut.songwriter_writes_song (songwriter_id, song_id) VALUES (%s, %s)", [songwriter_id, song_id])
 

        
            

        # return redirect(reverse('create_lagu', args=[album_id]))
        return HttpResponseRedirect(reverse('list_album_artist')) 
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nama FROM marmut.label")
        labels = cursor.fetchall()

        #jika is_artist true
        if not user_data['is_artist'] :
            print("dia bukan artist")
            cursor.execute("SELECT id, nama FROM marmut.artist JOIN marmut.akun ON artist.email_akun = akun.email")
            artists = cursor.fetchall()
        else:
           cursor.execute("SELECT id, nama FROM marmut.artist JOIN marmut.akun ON artist.email_akun = akun.email WHERE akun.email = %s", [email])
           artists = cursor.fetchall()
       
       #jika is_songwriter true
        #jika is_songwriter true
        if user_data['is_songwriter']:
            print(" songwriter adalah true")
            cursor.execute("""SELECT id, nama FROM marmut.songwriter 
            JOIN marmut.akun ON songwriter.email_akun = akun.email 
            WHERE akun.email != %s
        """, [email])
            songwriters = cursor.fetchall()
            cursor.execute("SELECT id, nama FROM marmut.songwriter JOIN marmut.akun ON songwriter.email_akun = akun.email WHERE akun.email = %s", [email])
           
            # Tambahkan data songwriter pengguna ke dalam list songwriters
            # user_songwriter = cursor.fetchone()
            # if user_songwriter:
            #     songwriters.append(user_songwriter)
        else:
            print("songwriter bukan trueee")
            cursor.execute("SELECT id, nama FROM marmut.songwriter JOIN marmut.akun ON songwriter.email_akun = akun.email")
            songwriters = cursor.fetchall()

        
        cursor.execute("SELECT DISTINCT genre FROM marmut.genre")
        genres = cursor.fetchall()

    context = {
        'labels': labels,
        'artists': artists,
        'songwriters': songwriters,
        'genres': genres,
    }
    return render(request, 'create_album.html', context)
