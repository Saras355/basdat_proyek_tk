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

from akun.views import list_tables

urlpatterns = [
    # path("admin/", admin.site.urls),
    # path('auth/', include('auth.urls')),
    path("admin/", admin.site.urls),
    path('akun/', include('akun.urls')),
    path('', akun_views.home, name='home'),
]
