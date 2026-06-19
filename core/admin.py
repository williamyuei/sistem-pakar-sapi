from django.contrib import admin
from .models import Penyakit, Gejala, Rule, NilaiCF, SolusiPenanganan


class RuleInline(admin.TabularInline):
    model = Rule
    extra = 1


class SolusiPenangananInline(admin.StackedInline):
    model = SolusiPenanganan
    extra = 0
    fields = ('jenis', 'judul', 'deskripsi', 'prioritas', 'aktif', 'referensi', 'catatan_khusus')


@admin.register(Penyakit)
class PenyakitAdmin(admin.ModelAdmin):
    list_display = ('kode', 'nama', 'jumlah_solusi')
    inlines = [RuleInline, SolusiPenangananInline]
    search_fields = ('kode', 'nama')
    
    def jumlah_solusi(self, obj):
        return obj.solusi_penanganan.filter(aktif=True).count()
    jumlah_solusi.short_description = 'Jumlah Solusi'


@admin.register(Gejala)
class GejalaAdmin(admin.ModelAdmin):
    list_display = ('kode', 'nama')
    search_fields = ('kode', 'nama')


@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = ('penyakit', 'gejala', 'cf_pakar')
    list_filter = ('penyakit',)
    search_fields = ('penyakit__nama', 'gejala__nama')


@admin.register(SolusiPenanganan)
class SolusiPenangananAdmin(admin.ModelAdmin):
    list_display = ('penyakit', 'jenis', 'judul', 'prioritas', 'aktif', 'diupdate')
    list_filter = ('jenis', 'aktif', 'penyakit')
    search_fields = ('judul', 'deskripsi', 'penyakit__nama')
    list_editable = ('prioritas', 'aktif')
    ordering = ('penyakit__kode', 'prioritas', 'jenis')
    
    fieldsets = (
        ('Informasi Dasar', {
            'fields': ('penyakit', 'jenis', 'judul', 'prioritas', 'aktif')
        }),
        ('Konten Solusi', {
            'fields': ('deskripsi',)
        }),
        ('Referensi & Catatan', {
            'fields': ('referensi', 'catatan_khusus'),
            'classes': ('collapse',)
        }),
    )


@admin.register(NilaiCF)
class NilaiCFAdmin(admin.ModelAdmin):
    list_display = ('nama_pemilik', 'nama_sapi', 'tanggal')
    readonly_fields = ('gejala_dipilih', 'hasil_cf', 'tanggal')
    list_filter = ('tanggal',)
    search_fields = ('nama_pemilik', 'nama_sapi')
