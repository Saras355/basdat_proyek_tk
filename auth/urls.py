from django.urls import path
from .views import *
app_name = 'auth'


urlpatterns = [
    path('', show_home, name='home'),
    path('register/', register_with_postgres, name='register' ),
    path('login/', login_with_postgres, name='login' ),
    path('logout/', logout_with_postgres, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
]