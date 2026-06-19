"""
Management command untuk mengisi data awal basis pengetahuan.
Jalankan: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from core.models import Penyakit, Gejala, Rule

PENYAKIT = [
    ("P01", "Anthrax",
     "Penyakit menular akut akibat bakteri Bacillus anthracis. Dapat menyebabkan kematian mendadak.",
     "Segera hubungi dokter hewan. Berikan antibiotik penisilin/tetrasiklin. Isolasi hewan dan laporkan ke dinas peternakan."),
    ("P02", "Penyakit Mulut dan Kuku (PMK)",
     "Penyakit viral sangat menular pada hewan berkuku belah, ditandai luka pada mulut dan kuku.",
     "Isolasi hewan, bersihkan luka dengan antiseptik. Vaksinasi rutin. Laporkan ke otoritas veteriner."),
    ("P03", "Brucellosis",
     "Penyakit bakteri (Brucella abortus) yang menyebabkan keguguran dan gangguan reproduksi.",
     "Tidak ada pengobatan efektif. Vaksinasi sapi muda, afkir hewan positif, sanitasi kandang."),
    ("P04", "Mastitis",
     "Peradangan kelenjar susu akibat infeksi bakteri (Staphylococcus/Streptococcus).",
     "Berikan antibiotik intramammary. Jaga kebersihan kandang dan proses pemerahan."),
    ("P05", "Bloat (Kembung Rumen)",
     "Penumpukan gas berlebih di rumen akibat fermentasi pakan yang terlalu cepat.",
     "Pasang selang rumen untuk mengeluarkan gas. Berikan minyak nabati atau simethicone. Atur pola pakan."),
]

GEJALA = [
    ("G01", "Demam tinggi (suhu > 40°C)"),
    ("G02", "Kematian mendadak tanpa gejala sebelumnya"),
    ("G03", "Pendarahan dari lubang tubuh (hidung, mulut, anus)"),
    ("G04", "Pembengkakan di leher atau dada"),
    ("G05", "Luka/lepuh pada mulut dan lidah"),
    ("G06", "Luka/lepuh pada kuku dan sela kuku"),
    ("G07", "Produksi air liur berlebihan"),
    ("G08", "Pincang / kesulitan berjalan"),
    ("G09", "Keguguran pada sapi bunting"),
    ("G10", "Radang sendi (bengkak pada persendian)"),
    ("G11", "Penurunan produksi susu"),
    ("G12", "Susu berubah warna / bernanah"),
    ("G13", "Ambing (kelenjar susu) bengkak dan panas"),
    ("G14", "Perut kiri membesar / kembung"),
    ("G15", "Sapi gelisah dan menendang-nendang perut"),
    ("G16", "Nafsu makan menurun drastis"),
    ("G17", "Lemas dan tidak mau bergerak"),
]

# (kode_penyakit, kode_gejala, cf_pakar)
RULES = [
    ("P01","G01",0.8), ("P01","G02",0.9), ("P01","G03",0.9), ("P01","G04",0.7), ("P01","G17",0.6),
    ("P02","G05",0.9), ("P02","G06",0.9), ("P02","G07",0.8), ("P02","G08",0.7), ("P02","G01",0.6), ("P02","G16",0.5),
    ("P03","G09",0.9), ("P03","G10",0.7), ("P03","G11",0.6), ("P03","G01",0.5), ("P03","G17",0.5),
    ("P04","G12",0.9), ("P04","G13",0.9), ("P04","G11",0.8), ("P04","G01",0.5),
    ("P05","G14",0.9), ("P05","G15",0.8), ("P05","G16",0.7), ("P05","G17",0.6),
]


class Command(BaseCommand):
    help = "Isi data awal penyakit, gejala, dan rule CF."

    def handle(self, *args, **kwargs):
        p_map = {}
        for kode, nama, desk, solusi in PENYAKIT:
            obj, created = Penyakit.objects.get_or_create(kode=kode, defaults={"nama": nama, "deskripsi": desk, "solusi": solusi})
            p_map[kode] = obj
            if created:
                self.stdout.write(f"  + Penyakit: {obj}")

        g_map = {}
        for kode, nama in GEJALA:
            obj, created = Gejala.objects.get_or_create(kode=kode, defaults={"nama": nama})
            g_map[kode] = obj
            if created:
                self.stdout.write(f"  + Gejala: {obj}")

        for kp, kg, cf in RULES:
            _, created = Rule.objects.get_or_create(penyakit=p_map[kp], gejala=g_map[kg], defaults={"cf_pakar": cf})
            if created:
                self.stdout.write(f"  + Rule: {kp}|{kg}|CF={cf}")

        self.stdout.write(self.style.SUCCESS("Seed data selesai!"))
