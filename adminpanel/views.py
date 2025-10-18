from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'templateadmin/loginAdmin.html')    

def blank_page(request):
    #return HttpResponse("ini halaman admin panel index")
    return render(request, 'templateadmin/blankPageAdmin.html')

def master_form(request):
    return render(request, 'templateadmin/masterFormAdmin.html')