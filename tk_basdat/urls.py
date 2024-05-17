"""
URL configuration for tk_basdat project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from akun import views as akun_views
from album_song_royalti.views import *
from akun.views import list_tables

urlpatterns = [
    path('', include('main.urls')),
    path('akun/', include('akun.urls')),
    path("admin/", admin.site.urls),
    path('akun/', include('akun.urls')),
    path('', akun_views.home, name='home'),
    # path('list_tables/', list_tables, name='list_tables'),
    path('album_song_royalti/', include('album_song_royalti.urls')),
    path("user_playlist/", include('user_playlist.urls')),
]
