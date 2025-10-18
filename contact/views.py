from django.shortcuts import render
from django.http import HttpResponse

from . import models
#from blog.models import Post

# Create your views here.
def index(request):
    context ={
        'title':'Index Contact',
        'Heading':'Ini adalah halaman index Contact',
    }
    return render(request,'contact/contactIndex.html', context)
    #return HttpResponse("ini halaman contact")

