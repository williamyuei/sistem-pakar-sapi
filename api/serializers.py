from rest_framework import serializers
from core.models import Gejala


class GejalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gejala
        fields = ['id', 'kode', 'nama']


class GejalaCFSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=1)
    cf_user = serializers.FloatField()

    def validate_cf_user(self, value):
        if value not in (0.0, 0.2, 0.4, 0.6, 0.8):
            raise serializers.ValidationError(
                "cf_user harus 0.8 (Yakin), 0.6 (Cukup Yakin), 0.4 (Sedikit Yakin), 0.2 (Tidak Tahu), atau 0.0 (Tidak)."
            )
        return value


class DiagnosaInputSerializer(serializers.Serializer):
    """Validasi input POST /api/diagnosa/"""
    gejala = GejalaCFSerializer(many=True, min_length=1)


class HasilCFSerializer(serializers.Serializer):
    """Output satu baris hasil CF."""
    penyakit = serializers.CharField()
    kode = serializers.CharField()
    deskripsi = serializers.CharField()
    solusi = serializers.CharField()
    cf = serializers.FloatField()
    persentase = serializers.FloatField()
