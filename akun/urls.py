from django.urls import path
from .views import *
app_name = 'akun'

urlpatterns = [
    path('login/', login_with_postgres, name='login' ),
    path('register_choice/', register_choice, name='register_choice'),
    path('dashboard/', dashboard, name='dashboard'),
    path('register/pengguna/', register_pengguna, name='register_pengguna'),
    path('register/label/', register_label, name='register_label'),
    path('logout/', logout_view, name='logout'),
]