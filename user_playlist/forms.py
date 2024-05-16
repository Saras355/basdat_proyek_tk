# from django.forms import ModelForm
# from user_playlist.models import Akun, Paket, Transaction, Premium, NonPremium, Konten, Genre, Podcaster, Podcast, Episode, Artist, Songwriter, Song, Akun_play_Song, Playlist_Song
# from user_playlist.models import Songwriter_write_Song, Downloaded_Song, Album, Label, Playlist, Chart, User_playlist, Pemilik_hak_cipta, Royalti, Akun_play_User_playlist

# class UserPlaylistForm(ModelForm):
#     class Meta:
#         model = User_playlist
#         fields = ["judul", "deskripsi"]

from django import forms

class AddUserPlaylistForm(forms.Form):
    judul = forms.CharField(max_length=100, label='Judul')
    deskripsi = forms.CharField(max_length=500, label='Deskripsi', widget=forms.Textarea)

class EditUserPlaylistForm(forms.Form):
    judul = forms.CharField(label='Judul', max_length=100)
    deskripsi = forms.CharField(label='Deskripsi', widget=forms.Textarea)