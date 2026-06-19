from django.urls import path
from .views import GejalaListAPI, DiagnosaAPI

urlpatterns = [
    path('gejala/', GejalaListAPI.as_view(), name='api-gejala'),
    path('diagnosa/', DiagnosaAPI.as_view(), name='api-diagnosa'),
]
