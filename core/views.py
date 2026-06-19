from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Gejala, NilaiCF
from .cf_engine import hitung_cf


def home(request):
    return render(request, 'home.html')


def login_view(request):
    """Login page untuk user"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f"Selamat datang, {user.get_full_name() or user.username}!")
            
            # Redirect ke halaman yang diminta sebelumnya atau ke home
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, "Username atau password salah.")
    
    return render(request, 'login.html')


def register_view(request):
    """Registration page untuk user baru"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        
        # Validasi
        if not username or not password1:
            messages.error(request, "Username dan password wajib diisi.")
            return redirect('register')
        
        if password1 != password2:
            messages.error(request, "Password tidak cocok.")
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username sudah digunakan.")
            return redirect('register')
        
        if email and User.objects.filter(email=email).exists():
            messages.error(request, "Email sudah digunakan.")
            return redirect('register')
        
        # Buat user baru
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )
        
        messages.success(request, "Akun berhasil dibuat! Silakan login.")
        return redirect('login')
    
    return render(request, 'register.html')


def logout_view(request):
    """Logout user"""
    auth_logout(request)
    messages.success(request, "Anda telah logout.")
    return redirect('home')


@login_required(login_url='login')
def diagnosa(request):
    """
    GET : Tampilkan form pilih gejala.
    POST: Hitung CF, simpan riwayat, redirect ke hasil.
    """
    if request.method == 'POST':
        nama_pemilik = request.POST.get('nama_pemilik', '').strip()
        nama_sapi = request.POST.get('nama_sapi', '').strip()
        gejala_ids = request.POST.getlist('gejala')

        if not nama_pemilik:
            messages.error(request, "Nama pemilik wajib diisi.")
            return redirect('diagnosa')

        if not gejala_ids:
            messages.error(request, "Pilih minimal satu gejala.")
            return redirect('diagnosa')

        gejala_ids = [int(i) for i in gejala_ids]
        hasil = hitung_cf(gejala_ids)

        if not hasil:
            messages.warning(request, "Tidak ada penyakit yang cocok dengan gejala yang dipilih.")
            return redirect('diagnosa')

        gejala_qs = Gejala.objects.filter(id__in=gejala_ids)
        riwayat = NilaiCF.objects.create(
            nama_pemilik=nama_pemilik,
            nama_sapi=nama_sapi,
            gejala_dipilih=list(gejala_qs.values('id', 'kode', 'nama')),
            hasil_cf=hasil,
        )
        return redirect('hasil', pk=riwayat.pk)

    gejala_list = Gejala.objects.all()
    return render(request, 'diagnosa.html', {'gejala_list': gejala_list})


@login_required(login_url='login')
def hasil(request, pk):
    riwayat = get_object_or_404(NilaiCF, pk=pk)
    return render(request, 'hasil.html', {'riwayat': riwayat})


@login_required(login_url='login')
def riwayat(request):
    # User hanya bisa lihat riwayat diagnosa mereka sendiri (berdasarkan nama pemilik)
    # Atau jika superuser, bisa lihat semua
    if request.user.is_superuser or request.user.is_staff:
        data = NilaiCF.objects.all()
    else:
        # Filter berdasarkan username atau nama lengkap user
        user_name = request.user.get_full_name() or request.user.username
        data = NilaiCF.objects.filter(nama_pemilik__icontains=user_name)
    
    return render(request, 'riwayat.html', {'data': data})
