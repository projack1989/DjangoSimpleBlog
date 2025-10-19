from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.hashers import check_password

from .models import TmUser
from .forms import RegisterTmUser, LoginTmUser

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
                request.session['user_id'] = user.s_id_user
                request.session['user_name'] = user.s_first_name
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
        return redirect('login')
    return render(request, 'templateadmin/blankPageAdmin.html', {
        'user_name': request.session.get('user_name')
    })

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