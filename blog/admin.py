from django.contrib import admin
#from .models import SliderBanner,Artikel1
from . import models
# Register your models here.

@admin.register(models.SliderBanner)
class SliderBanner(admin.ModelAdmin):
    list_display = (
        's_id_slider_banner',
        's_nama_gambar',
        's_description',
        'n_istatus',
        's_created_on'
    )
    list_filter = ('n_istatus',)
    search_fields = ('s_nama_gambar',)

@admin.register(models.Artikel1)
class SliderBanner(admin.ModelAdmin):
    list_display = (
        's_id_article',
        's_title',
        's_description',
        'd_created_on',
        's_created_by',
        'd_updated_on',
        'n_istatus',
    )
    list_filter = ('n_istatus',)
    search_fields = ('s_description',)
