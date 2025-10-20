from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.hashers import check_password
from django.utils import timezone

from .models import TmUser
from .forms import RegisterTmUser, LoginTmUser, SliderBannerForm, Artikel1Form
from blog import models as blog_models
from about import models as about_models
from about.forms import AboutForm

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
    #print('session:', request.session.__dict__)
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

def about(request):
    tampilAbout = about_models.About.objects.filter(n_istatus__in=['1','0']).values(
        's_id_about','s_title','s_description','d_created_on','s_created_by','n_istatus'
    ).order_by('-d_created_on')
    #print(tampilAbout)
    context ={
        'tampilAbout': tampilAbout,
        'header':'Halaman About',
    }
    #pass
    #return HttpResponse("halaman sliderImage")
    return render(request, 'templateadmin/listAboutAdmin.html',context)

def editAbout(request, s_id_about):
    about = get_object_or_404(about_models.About, s_id_about=s_id_about)
    if request.method == 'POST':
        form = AboutForm(request.POST, request.FILES, instance=about)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data berhasil diperbarui!')
            return redirect('adminpanel:about')
        else:
            messages.error(request, 'Periksa kembali form yang kamu isi.')
    else:
        form = AboutForm(instance=about)
    return render(request, 'templateadmin/editAboutAdmin.html', {
        'form': form,
        'about': about
    })

def addAbout(request):
    if request.method == 'POST':
        # === VALIDASI MANUAL ===
        form = AboutForm(request.POST)
        #print('form errors:', form.errors)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data berhasil diperbarui!')
            return redirect('adminpanel:about')
        else:
            messages.error(request, 'Periksa kembali form yang kamu isi.')
    else:
        form = AboutForm()
    context = {
        'judul': 'Tambah Artikel About',
        'form': form,
    }
        
    return render(request, 'templateadmin/addAboutAdmin.html',context)

    

def addAbout2(request):
    if request.method == 'POST':
        s_title = request.POST.get('s_title', '').strip()
        s_description = request.POST.get('s_description', '').strip()
        n_istatus = request.POST.get('n_istatus', '1')
        s_created_by = request.session.get('s_email')  # contoh ambil dari session

        # === VALIDASI MANUAL ===
        errors = {}

        # Validasi title
        if not s_title:
            errors['s_title'] = "Judul tidak boleh kosong."
        elif len(s_title) > 200:
            errors['s_title'] = "Judul terlalu panjang, maksimal 200 karakter."

        # Validasi deskripsi
        if not s_description:
            errors['s_description'] = "Deskripsi tidak boleh kosong."
        elif len(s_description) < 10:
            errors['s_description'] = "Deskripsi minimal 10 karakter."

        # Jika ada error → tampilkan lagi form dengan pesan
        if errors:
            return render(request, 'templateadmin/addAboutAdmin.html', {
                'errors': errors,
                'values': request.POST
            })

        # Simpan ke database
        about_models.About.objects.create(
            s_title=s_title,
            s_description=s_description,
            s_created_by=s_created_by,
            d_created_on=timezone.now().date(),
            n_istatus=n_istatus
        )

        messages.success(request, "Artikel About berhasil ditambahkan!")
        return redirect('adminpanel:about')

    return render(request, 'templateadmin/addAboutAdmin.html')

def article(request):
    tampilArtikel = blog_models.Artikel1.objects.filter(n_istatus__in=['1','0']).values(
        's_id_article','s_title','s_description','d_created_on','s_created_by','n_istatus'
    ).order_by('-d_created_on')
    print(tampilArtikel)
    context ={
        'tampilArtikel': tampilArtikel,
        'header':'Halaman Article',
    }
    #pass
    #return HttpResponse("halaman sliderImage")
    return render(request, 'templateadmin/listArticleAdmin.html',context)

def editArticle(request, s_id_article):
    article = get_object_or_404(blog_models.Artikel1, s_id_article=s_id_article)
    if request.method == 'POST':
        form = Artikel1Form(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Edit Artikel berhasil diperbarui!')
            return redirect('adminpanel:article')
        else:
            messages.error(request, 'Periksa kembali form yang kamu isi.')
    else:
        form = Artikel1Form(instance=article)
        #print(form)
    context = {
        'judul': 'Edit Artikel',
        'form': form,
    }
    return render(request, 'templateadmin/editArticleAdmin.html', context)

def deleteArticle(request, s_id_article):
    article = get_object_or_404(blog_models.Artikel1, s_id_article=s_id_article)
    # Hapus data dari database
    article.delete()
    messages.success(request, "Data Artikel berhasil dihapus.")
    return redirect('adminpanel:article')  # arah

def addArticle(request):
    if request.method == 'POST':
        # === VALIDASI MANUAL ===
        form = Artikel1Form(request.POST)
        #print('form errors:', form.errors)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data berhasil diperbarui!')
            return redirect('adminpanel:article')
        else:
            messages.error(request, 'Periksa kembali form yang kamu isi.')
    else:
        form = Artikel1Form()
    context = {
        'judul': 'Tambah Artikel',
        'form': form,
    }

    return render(request, 'templateadmin/addArticleAdmin.html',context)
