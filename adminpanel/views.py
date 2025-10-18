from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("ini halaman admin panel index")

def about(request):
    return HttpResponse("ini halaman admin panel 2")