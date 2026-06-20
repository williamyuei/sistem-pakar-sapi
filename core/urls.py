from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('diagnosa/', views.diagnosa, name='diagnosa'),
    path('diagnosa/konfirmasi/', views.konfirmasi, name='konfirmasi'),
    path('hasil/<int:pk>/', views.hasil, name='hasil'),
    path('riwayat/', views.riwayat, name='riwayat'),
]
