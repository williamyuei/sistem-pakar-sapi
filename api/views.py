from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.models import Gejala
from core.cf_engine import hitung_cf
from .serializers import GejalaSerializer, DiagnosaInputSerializer, HasilCFSerializer


class GejalaListAPI(APIView):
    """
    GET /api/gejala/
    Mengembalikan seluruh daftar gejala.
    """
    def get(self, request):
        data = GejalaSerializer(Gejala.objects.all(), many=True).data
        return Response(data)


class DiagnosaAPI(APIView):
    """
    POST /api/diagnosa/
    Body : {"gejala": [{"id": 1, "cf_user": 0.8}, {"id": 3, "cf_user": 0.6}, ...]}
    Return: list hasil CF diurutkan dari tertinggi.
    """
    def post(self, request):
        serializer = DiagnosaInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        gejala_cf = {item['id']: item['cf_user'] for item in serializer.validated_data['gejala']}
        hasil = hitung_cf(gejala_cf)
        if not hasil:
            return Response(
                {"detail": "Tidak ada penyakit yang cocok."},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(HasilCFSerializer(hasil, many=True).data)
