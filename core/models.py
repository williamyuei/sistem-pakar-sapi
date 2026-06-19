from django.db import models


class Penyakit(models.Model):
    """Entitas penyakit yang dapat didiagnosis oleh sistem."""
    kode = models.CharField(max_length=10, unique=True)
    nama = models.CharField(max_length=150)
    deskripsi = models.TextField()
    solusi = models.TextField(help_text="Saran penanganan awal")

    def __str__(self):
        return f"{self.kode} - {self.nama}"

    class Meta:
        verbose_name_plural = "Penyakit"
        ordering = ['kode']


class Gejala(models.Model):
    """Entitas gejala yang dapat dipilih pengguna saat konsultasi."""
    kode = models.CharField(max_length=10, unique=True)
    nama = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.kode} - {self.nama}"

    class Meta:
        verbose_name_plural = "Gejala"
        ordering = ['kode']


class Rule(models.Model):
    """
    Aturan basis pengetahuan: relasi antara Penyakit dan Gejala.
    Setiap rule menyimpan nilai CF (Certainty Factor) dari pakar.
    """
    penyakit = models.ForeignKey(Penyakit, on_delete=models.CASCADE, related_name='rules')
    gejala = models.ForeignKey(Gejala, on_delete=models.CASCADE, related_name='rules')
    cf_pakar = models.FloatField(help_text="Nilai CF dari pakar (0.0 – 1.0)")

    def __str__(self):
        return f"{self.penyakit.kode} | {self.gejala.kode} | CF={self.cf_pakar}"

    class Meta:
        verbose_name = "Rule CF"
        verbose_name_plural = "Rule CF"
        unique_together = ('penyakit', 'gejala')


class SolusiPenanganan(models.Model):
    """
    Solusi penanganan detail untuk setiap penyakit.
    Dapat ada multiple solusi per penyakit (misal: pencegahan, pengobatan, dll).
    """
    JENIS_CHOICES = [
        ('pengobatan', 'Pengobatan'),
        ('pencegahan', 'Pencegahan'),
        ('manajemen', 'Manajemen Hewan'),
        ('sanitasi', 'Sanitasi & Biosecurity'),
        ('vaksinasi', 'Vaksinasi'),
        ('nutrisi', 'Nutrisi & Suplemen'),
    ]
    
    penyakit = models.ForeignKey(Penyakit, on_delete=models.CASCADE, related_name='solusi_penanganan')
    jenis = models.CharField(max_length=20, choices=JENIS_CHOICES, help_text="Jenis solusi penanganan")
    judul = models.CharField(max_length=200, help_text="Judul singkat solusi")
    deskripsi = models.TextField(help_text="Deskripsi lengkap solusi")
    prioritas = models.IntegerField(default=1, help_text="Prioritas urutan tampil (1=tertinggi)")
    aktif = models.BooleanField(default=True, help_text="Aktifkan solusi ini")
    
    # Metadata
    referensi = models.TextField(blank=True, help_text="Sumber referensi (opsional)")
    catatan_khusus = models.TextField(blank=True, help_text="Catatan tambahan (opsional)")
    dibuat = models.DateTimeField(auto_now_add=True)
    diupdate = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.penyakit.kode} - {self.get_jenis_display()}: {self.judul}"
    
    class Meta:
        verbose_name = "Solusi Penanganan"
        verbose_name_plural = "Solusi Penanganan"
        ordering = ['penyakit__kode', 'prioritas', 'jenis']


class NilaiCF(models.Model):
    """
    Riwayat hasil konsultasi.
    Menyimpan gejala yang dipilih dan hasil perhitungan CF dalam format JSON.
    """
    nama_pemilik = models.CharField(max_length=100)
    nama_sapi = models.CharField(max_length=100, blank=True)
    tanggal = models.DateTimeField(auto_now_add=True)
    gejala_dipilih = models.JSONField()   # list of {id, kode, nama}
    hasil_cf = models.JSONField()         # list of {penyakit, kode, cf, persentase, ...}

    def __str__(self):
        return f"{self.nama_pemilik} — {self.tanggal.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        verbose_name = "Hasil Konsultasi"
        verbose_name_plural = "Riwayat Konsultasi"
        ordering = ['-tanggal']
