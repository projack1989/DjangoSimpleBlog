from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from . import models as AboutModels
#from blog import models as BlogModels
#from about import models as AboutModels
from blog.global_page import GlobalPageMixin

# Create your views here.
class IndexView(GlobalPageMixin,TemplateView):
    template_name = 'about/aboutIndex.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Index About'
        context['Heading'] = 'Ini adalah halaman About - Index'
        context['aboutList'] = AboutModels.About.objects.filter(n_istatus='1')
        #print("DEBUG ABOUT DATA:", context['aboutList'])  # debug
        return context