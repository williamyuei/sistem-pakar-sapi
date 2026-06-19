from rest_framework import serializers
from core.models import Gejala


class GejalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gejala
        fields = ['id', 'kode', 'nama']


class DiagnosaInputSerializer(serializers.Serializer):
    """Validasi input POST /api/diagnosa/"""
    gejala_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        min_length=1,
        error_messages={'min_length': 'Pilih minimal satu gejala.'}
    )


class HasilCFSerializer(serializers.Serializer):
    """Output satu baris hasil CF."""
    penyakit = serializers.CharField()
    kode = serializers.CharField()
    deskripsi = serializers.CharField()
    solusi = serializers.CharField()
    cf = serializers.FloatField()
    persentase = serializers.FloatField()
