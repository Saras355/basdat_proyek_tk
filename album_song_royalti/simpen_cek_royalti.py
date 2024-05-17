def cek_royalti(request):
    user_data = request.session.get('user_data', {})
    user_email = user_data.get('email', '')

    if user_data.get('is_label'):
        with connection.cursor() as cursor:
            cursor.execute("""
            SET SEARCH_PATH TO MARMUT;
            SELECT
              S.id_konten AS id_song,
              PHC.id AS id_pemilik_hak_cipta,
              (CAST(S.total_play AS NUMERIC) * CAST(PHC.rate_royalti AS NUMERIC)) AS TotalRoyalti
            FROM
              LABEL L
              JOIN ALBUM A ON L.id = A.id_label
              JOIN SONG S ON S.id_album = A.id
              JOIN KONTEN K ON K.id = S.id_konten
              JOIN PEMILIK_HAK_CIPTA PHC ON L.id_pemilik_hak_cipta = PHC.id
            WHERE
              L.email = %s
            """, [user_email])
            royalty_data = cursor.fetchall()

            # Update the ROYALTI table for each song
            for row in royalty_data:
                id_song = row[0]
                id_pemilik_hak_cipta = row[1]
                total_royalti = row[2]

                cursor.execute("""
                UPDATE ROYALTI
                SET jumlah = %s
                WHERE id_pemilik_hak_cipta = %s AND id_song = %s
                """, [total_royalti, id_pemilik_hak_cipta, id_song])

    context = {
        'royalty_list': royalty_data
    }
    return render(request, 'cek_royalti.html', context)
