--Nomor 1
--pengecekan email
SET SEARCH_PATH TO MARMUT;
CREATE OR REPLACE FUNCTION cek_email_terdaftar() RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS(SELECT 1 FROM akun WHERE NEW.email = email) THEN
        RAISE EXCEPTION 'Email sudah terdaftar';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
SET SEARCH_PATH TO MARMUT;
CREATE TRIGGER trg_cek_email_terdaftar
BEFORE INSERT ON akun
FOR EACH ROW
EXECUTE FUNCTION cek_email_terdaftar();

-- pendaftaran pengguna baru
-- harunsya ga perlu dispesifikin penggunanya(?)
SET SEARCH_PATH TO MARMUT;
CREATE OR REPLACE FUNCTION set_non_premium() RETURNS TRIGGER AS $$
BEGIN
    NEW.is_premium := false;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
SET SEARCH_PATH TO MARMUT;
CREATE TRIGGER trg_set_non_premium
BEFORE INSERT ON akun
FOR EACH ROW
-- WHEN (NEW.role = 'Pengguna') -- ini tidak vliad dan ini juga ga bisa diakses oleh usernya  yg bukan pengguna seperit lable
EXECUTE FUNCTION set_non_premium();


-- memerikasa status langganan pengguna
SET SEARCH_PATH TO MARMUT;
CREATE OR REPLACE FUNCTION cek_status_langganan() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status_langganan = 'Premium' AND NEW.timestamp_berakhir > CURRENT_DATE THEN
        NEW.status_langganan := 'Non Premium';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
SET SEARCH_PATH TO MARMUT;
CREATE TRIGGER trg_cek_status_langganan
BEFORE UPDATE ON akun
FOR EACH ROW
EXECUTE FUNCTION cek_status_langganan();


-- Nomor 2
-- Memperbarui atribut durasi dan jumlah lagu
CREATE OR REPLACE FUNCTION update_user_playlist_data()
RETURNS TRIGGER AS
$$
DECLARE
    total_duration INT;
    total_songs INT;
BEGIN
    SELECT SUM(k.durasi), COUNT(*)
    INTO total_duration, total_songs
    FROM marmut.playlist_song ps
    JOIN marmut.song s ON ps.id_song = s.id_konten
    JOIN marmut.konten k ON s.id_konten = k.id
    WHERE ps.id_playlist = COALESCE(NEW.id_playlist, OLD.id_playlist);

    UPDATE marmut.user_playlist
    SET total_durasi = COALESCE(total_duration, 0),
        jumlah_lagu = total_songs
    WHERE id_playlist = COALESCE(NEW.id_playlist, OLD.id_playlist);

    RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER update_user_playlist_data_trigger
AFTER INSERT OR DELETE ON marmut.playlist_song
FOR EACH ROW EXECUTE FUNCTION update_user_playlist_data();




-- Memeriksa lagu ganda pada playlist
CREATE OR REPLACE FUNCTION check_duplicate_song()
RETURNS TRIGGER AS
$$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM marmut.playlist_song
        WHERE id_playlist = NEW.id_playlist AND id_song = NEW.id_song
    ) THEN
        RAISE EXCEPTION 'Lagu sudah ada dalam playlist';
    END IF;

    RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER check_duplicate_song_trigger
BEFORE INSERT ON marmut.playlist_song
FOR EACH ROW EXECUTE FUNCTION check_duplicate_song();


--memeriksa lagu ganda pada download song
SET SEARCH_PATH TO MARMUT;
CREATE OR REPLACE FUNCTION cek_lagu_ganda_downloaded_song() RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS(
        SELECT 1
        FROM downloaded_song
        WHERE id_song = NEW.id_song
          AND email_downloader = NEW.email_downloader
    ) THEN
        RAISE EXCEPTION 'Lagu sudah diunduh sebelumnya';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
SET SEARCH_PATH TO MARMUT;
CREATE TRIGGER trg_cek_lagu_ganda_downloaded_song
BEFORE INSERT ON downloaded_song
FOR EACH ROW
EXECUTE FUNCTION cek_lagu_ganda_downloaded_song();


-- Nomor 3
-- Manajemen Langganan Paket
SET SEARCH_PATH TO MARMUT;
CREATE OR REPLACE FUNCTION cek_langganan_aktif() RETURNS TRIGGER AS $$
DECLARE
    langganan_aktif INT;
BEGIN
    SELECT COUNT(*) INTO langganan_aktif
    FROM transaction
    WHERE email = NEW.email
      AND timestamp_berakhir > CURRENT_TIMESTAMP;

    IF langganan_aktif > 0 THEN
        RAISE EXCEPTION 'Anda sudah memiliki langganan yang aktif';
    ELSE
        INSERT INTO premium (email)
        VALUES (NEW.email);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
SET SEARCH_PATH TO MARMUT;
CREATE TRIGGER trg_cek_langganan_aktif
BEFORE INSERT ON transaction
FOR EACH ROW
EXECUTE FUNCTION cek_langganan_aktif();

-- Manajemen Play User Playlist
SET SEARCH_PATH TO MARMUT;
CREATE OR REPLACE FUNCTION manajemen_play_user_playlist() RETURNS TRIGGER AS $$
DECLARE
    lagu RECORD;
BEGIN
    FOR lagu IN SELECT id_song FROM playlist_song WHERE id_playlist = NEW.id_playlist LOOP
        INSERT INTO akun_play_song (email_pemain, id_song, waktu)
        VALUES (NEW.email_pembuat, lagu.id_song, CURRENT_TIMESTAMP);
    END LOOP;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;
SET SEARCH_PATH TO MARMUT;
CREATE TRIGGER trg_manajemen_play_user_playlist
AFTER INSERT ON akun_play_user_playlist
FOR EACH ROW
EXECUTE FUNCTION manajemen_play_user_playlist();


-- Nomor 4
-- Memperbarui total play saat menambahkan lagu ke playlist
SET SEARCH_PATH TO MARMUT;
CREATE OR REPLACE FUNCTION update_total_play() RETURNS TRIGGER AS $$
BEGIN
    UPDATE song
    SET total_play = total_play + 1
    WHERE id_konten = NEW.id_song;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
SET SEARCH_PATH TO MARMUT;
CREATE TRIGGER trg_update_total_play
AFTER INSERT ON playlist_song
FOR EACH ROW
WHEN (pg_trigger_depth() = 0)
EXECUTE FUNCTION update_total_play();

--  Memperbarui total download
SET SEARCH_PATH TO MARMUT;
CREATE OR REPLACE FUNCTION update_total_download() RETURNS TRIGGER AS $$
BEGIN
    UPDATE song
    SET total_download = total_download + 1
    WHERE id_konten = NEW.id_song;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
SET SEARCH_PATH TO MARMUT;
CREATE TRIGGER trg_update_total_download
AFTER INSERT ON downloaded_song
FOR EACH ROW
WHEN (pg_trigger_depth() = 0)
EXECUTE FUNCTION update_total_download();


-- Nomor 5
-- Memperbarui durasi saat menambahkan atau menghapus episode dalam podcast
SET SEARCH_PATH TO MARMUT;
CREATE OR REPLACE FUNCTION update_podcast_duration() RETURNS TRIGGER AS $$
DECLARE
    total_duration INTEGER;
BEGIN
    -- Hitung total durasi dari semua episode yang terkait dengan podcast tersebut
    SELECT SUM(durasi) INTO total_duration
    FROM episode
    WHERE id_konten_podcast = NEW.id_konten;

    -- Update atribut durasi dari podcast dalam tabel KONTEN
    UPDATE konten
    SET durasi = total_duration
    WHERE id = NEW.id_konten;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


SET SEARCH_PATH TO MARMUT;
CREATE TRIGGER trg_update_podcast_duration
AFTER INSERT OR DELETE ON episode
FOR EACH ROW
WHEN (pg_trigger_depth() = 0)
EXECUTE FUNCTION update_podcast_duration();
SET SEARCH_PATH TO MARMUT;
-- Memperbarui atribut durasi dan jumlah lagu
SET SEARCH_PATH TO marmut;

CREATE OR REPLACE FUNCTION marmut.update_album_attributes()
RETURNS TRIGGER AS $$
DECLARE
    total_duration INT;
BEGIN
    -- Menghitung total durasi dengan join antara song dan konten
    SELECT SUM(K.durasi) INTO total_duration
    FROM marmut.song S
    JOIN marmut.konten K ON S.id_konten = K.id
    WHERE S.id_album = NEW.id;
    -- Menghitung jumlah lagu
    SELECT COUNT(*) INTO total_songs
    FROM marmut.song
    WHERE id_album = NEW.id_album;

    -- Memperbarui tabel album dengan total durasi
    UPDATE marmut.album
    SET total_durasi = total_duration, jumlah_lagu = total_songs
    WHERE id = NEW.id_album;
    RAISE NOTICE 'Album ID: %, Total Durasi: %, Jumlah Lagu: %', NEW.id_album, total_duration, total_songs
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

SET SEARCH_PATH TO MARMUT;
CREATE TRIGGER trg_update_album_attributes
AFTER INSERT OR DELETE ON marmut.song
FOR EACH ROW
-- WHEN (pg_trigger_depth() = 0)
EXECUTE FUNCTION update_album_attributes();

