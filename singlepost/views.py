from django.shortcuts import render
from django.http import HttpResponse

from . import models
#from blog.models import Post

# Create your views here.
def index(request):
    context ={
        'title':'Index Single Post',
        'Heading':'Ini adalah halaman index Single Post',
    }
    return render(request,'singlepost/singlePostIndex.html', context)
    #return HttpResponse("ini halaman singlePost")

