from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core import serializers
from user_playlist.forms import UserPlaylistForm
from django.urls import reverse
from user_playlist.models import User_playlist
# from connect_postgres import execute_sql_query, execute_sql_query_no_fetch
import uuid

def show_user_playlist(request):
    query = """
    SELECT * FROM USER_PLAYLIST;
    """
    playlists = User_playlist.objects.all()
    context = {'playlists': playlists}
    return render(request, 'show_user_playlist.html', context)

def playlist_detail(request, playlist_id):
    try:
        playlist = User_playlist.objects.get(id_User_playlist=playlist_id)
        context = {'playlist': playlist}
        return render(request, 'playlist_detail.html', context)
    except User_playlist.DoesNotExist:
        return HttpResponse("Playlist not found.")

def delete_playlist(request, playlist_id):
    try:
        playlist = User_playlist.objects.get(id_User_playlist=playlist_id)
        playlist.delete()
        return redirect('main:show_user_playlist')
    except User_playlist.DoesNotExist:
        return HttpResponse("Playlist not found.")

def edit_playlist(request, playlist_id):
    try:
        playlist = User_playlist.objects.get(id_User_playlist=playlist_id)
        if request.method == 'POST':
            form = UserPlaylistForm(request.POST, instance=playlist)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('main:playlist_detail', args=[playlist_id]))
            else:
                # If form is not valid, render the form with errors
                return render(request, 'edit_playlist.html', {'form': form})
        else:
            form = UserPlaylistForm(instance=playlist)
            return render(request, 'edit_playlist.html', {'form': form})
    except User_playlist.DoesNotExist:
        return HttpResponse("Playlist not found.")

def add_playlist(request):
    form = UserPlaylistForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('main:show_user_playlist'))

    context = {'form': form}
    return render(request, "add_playlist.html", context)

def add_playlist(request):
    form = UserPlaylistForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('main:show_user_playlist'))

    context = {'form': form}
    return render(request, "add_playlist.html", context)