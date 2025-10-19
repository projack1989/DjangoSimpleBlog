from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.hashers import check_password
from django.utils import timezone

from .models import TmUser
from .forms import RegisterTmUser, LoginTmUser, SliderBannerForm
from blog import models as blog_models

import os

# Create your views here.
def index(request):
    form = LoginTmUser(request.POST or None)
    if request.method == 'POST':
        email = request.POST['s_email']
        password = request.POST['s_password']

        try:
            user = TmUser.objects.get(s_email=email)
            #cekpwd = check_password(password, user.s_password)
            #print(cekpwd)
            if check_password(password, user.s_password):
                #pada Django wajib request atau set session supaya bisa digunakan pada function lainnya
                request.session['user_id'] = user.s_id_user
                request.session['s_first_name'] = user.s_first_name
                request.session['s_last_name'] = user.s_last_name
                request.session['s_email'] = user.s_email
                messages.success(request, f"Selamat datang, {user.s_first_name}!")
                #return HttpResponse("sukses Login")
                return redirect('adminpanel:blank-page')
            else:
                #return HttpResponse("password salah")
                messages.error(request, "Password salah.")
        except TmUser.DoesNotExist:
            #return HttpResponse("email tidak ditemukan")
            messages.error(request, "Email tidak ditemukan.")
    return render(request, 'templateadmin/loginAdmin.html', {'form': form})
    #return render(request, 'templateadmin/loginAdmin.html')    

def blank_page(request):
    #return HttpResponse("ini halaman admin panel index")
    if not request.session.get('user_id'):
        return redirect('adminpanel:index')
        #return redirect('adminpanel:forgot-password')
    context ={
        's_email': request.session.get('s_email'),
    }
    #cara cek semua session yang ada pada Django    
    print('session:', request.session.__dict__)
    return render(request, 'templateadmin/blankPageAdmin.html', context)

def master_form(request):
    return render(request, 'templateadmin/masterFormAdmin.html')

def register(request):
    if request.method == 'POST':
        form = RegisterTmUser(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminpanel:index')
    else:
        form = RegisterTmUser()
    return render(request, 'templateadmin/registerPage.html', {'form': form})
    #return render(request, 'templateadmin/registerPage.html')

def forgot_password(request):
    return render(request, 'templateadmin/forgotPassword.html')

def logout(request):
    request.session.flush()
    messages.success(request, "Anda telah logout.")
    return redirect('adminpanel:index')

def sliderImage(request):
    #tampilSliderImage =blog_models.SliderBanner.objects.all()
    tampilSliderImage = blog_models.SliderBanner.objects.filter(n_istatus__in=['1','0']).values(
        's_id_slider_banner','s_nama_gambar','s_description','s_created_on','s_created_by','n_istatus'
    ).order_by('-s_created_on')
    context ={
        'tampilSliderImage': tampilSliderImage,
        #'MEDIA_URL': settings.MEDIA_URL,
    }
    #pass
    #return HttpResponse("halaman sliderImage")
    return render(request, 'templateadmin/sliderImageAdmin.html', context)

def editSlider(request, s_id_slider_banner):
    slider = get_object_or_404(blog_models.SliderBanner, s_id_slider_banner=s_id_slider_banner)
    if request.method == 'POST':
        form = SliderBannerForm(request.POST, request.FILES, instance=slider)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data berhasil diperbarui!')
            return redirect('adminpanel:slider-image')
        else:
            messages.error(request, 'Periksa kembali form yang kamu isi.')
    else:
        form = SliderBannerForm(instance=slider)
    return render(request, 'templateadmin/editSliderAdmin.html', {
        'form': form,
        'slider': slider
    })
    #return HttpResponse("halaman editSlider")

def deleteSlider(request, s_id_slider_banner):
    slider = get_object_or_404(blog_models.SliderBanner, pk=s_id_slider_banner)

    # Hapus file gambar fisik dari media folder
    if slider.s_nama_gambar:
        image_path = slider.s_nama_gambar.path
        if os.path.exists(image_path):
            os.remove(image_path)

    # Hapus data dari database
    slider.delete()
    messages.success(request, "Data slider berhasil dihapus.")
    return redirect('adminpanel:slider-image')  # arahkan kembali ke halaman utama list

def addSlider(request):
    if request.method == 'POST':
        s_nama_gambar = request.FILES.get('s_nama_gambar')
        s_description = request.POST.get('s_description', '').strip()
        n_istatus = request.POST.get('n_istatus', '1')
        s_created_by = request.session.get('s_email', 'admin')  # contoh ambil dari session

        # === VALIDASI MANUAL ===
        errors = {}

        # Validasi gambar
        if not s_nama_gambar:
            errors['s_nama_gambar'] = "Kamu belum memilih gambar."
        else:
            if not s_nama_gambar.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                errors['s_nama_gambar'] = "File gambar harus JPG atau PNG."
            elif s_nama_gambar.size > 2 * 1024 * 1024:
                errors['s_nama_gambar'] = "Ukuran gambar maksimal 2MB."

        # Validasi deskripsi
        if not s_description:
            errors['s_description'] = "Deskripsi tidak boleh kosong."
        elif len(s_description) < 10:
            errors['s_description'] = "Deskripsi minimal 10 karakter."

        # Jika ada error → tampilkan lagi form dengan pesan
        if errors:
            return render(request, 'templateadmin/addSliderAdmin.html', {
                'errors': errors,
                'values': request.POST
            })

        # Simpan ke database
        blog_models.SliderBanner.objects.create(
            s_nama_gambar=s_nama_gambar,
            s_description=s_description,
            s_created_by=request.session.get('s_email'),
            s_created_on=timezone.now().date(),
            n_istatus=n_istatus
        )

        messages.success(request, "Slider banner berhasil ditambahkan!")
        return redirect('adminpanel:slider-image')

    return render(request, 'templateadmin/addSliderAdmin.html')