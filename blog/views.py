from django.shortcuts import render
from django.http import HttpResponse

from django.views.generic import TemplateView
#from .models import SliderBanner
from blog.global_page import GlobalPageMixin

from . import models
#from blog.models import Post

# Create your views here.
def index(request):
    context ={
        'title':'Index Blog',
        'Heading':'Ini adalah halaman index blog',
    }

    return render(request,'blog/blogIndex.html', context)

class IndexView(GlobalPageMixin,TemplateView):
    template_name = 'blog/blogIndex.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Index Blog'
        context['Heading'] = 'Ini adalah halaman index blog'
        return context
