from django.forms import ModelForm
from user_playlist.models import Akun, Paket, Transaction, Premium, NonPremium, Konten, Genre, Podcaster, Podcast, Episode, Artist, Songwriter, Song, Akun_play_Song, Playlist_Song
from user_playlist.models import Songwriter_write_Song, Downloaded_Song, Album, Label, Playlist, Chart, User_playlist, Pemilik_hak_cipta, Royalti, Akun_play_User_playlist

class UserPlaylistForm(ModelForm):
    class Meta:
        model = User_playlist
        fields = ["judul", "deskripsi"]
