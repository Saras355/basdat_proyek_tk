from django.urls import path
from .views import *
app_name = 'akun'


urlpatterns = [
    path('list_tables/', list_tables, name='list_tables'),
    # path('register/', register_with_postgres, name='register' ),
    path('login/', login_with_postgres, name='login' ),
    path('register_choice/', register_choice, name='register_choice'),
    # path('register_pengguna/<str:role>/', register_pengguna, name='register'),
    # path('logout/', logout_with_postgres, name='logout'),
    # path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/', dashboard, name='dashboard'),
    path('register/pengguna/', register_pengguna, name='register_pengguna'),
    path('register/label/', register_label, name='register_label'),
]