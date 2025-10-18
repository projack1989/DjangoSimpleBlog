from django.contrib import admin
#from .models import SliderBanner,Artikel1
from . import models
# Register your models here.

@admin.register(models.About)
class About(admin.ModelAdmin):
    list_display = (
        's_id_about',
        's_title',
        's_description',
        'd_created_on',
        's_created_by',
        'd_updated_on',
        's_updated_by',
        'n_istatus', 
    )
    list_filter = ('s_id_about',)
    search_fields = ('s_title',)
