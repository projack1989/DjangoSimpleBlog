from django.db import models
from django.utils import timezone
    
class SliderBanner(models.Model):
    STATUS_CHOICES = (
        ('0', "Non Aktif"),
        ('1', "Aktif"),
    )

    s_id_slider_banner = models.BigAutoField(primary_key=True)
    #s_nama_gambar = models.CharField(max_length=100)
    s_nama_gambar = models.ImageField(upload_to='slider_banners/', blank=False, null=False) 
    s_created_on = models.DateField()
    s_description = models.TextField(null=True,blank=True,max_length=200)
    s_created_by = models.CharField(null=True, max_length=50)
    d_updated_on = models.DateField(null=True,blank=True)
    s_updated_by = models.CharField(null=True,blank=True, max_length=50)
    n_istatus = models.CharField(max_length=1, choices=STATUS_CHOICES, default='1')

    class Meta:
        db_table = 'tm_slider_banner'   # ⬅️ Nama tabel manual
        verbose_name = 'Slider Banner'
        verbose_name_plural = 'Slider Banners'

    def __str__(self):
        return f"{self.s_nama_gambar} ({self.get_n_istatus_display()})"
    
class Artikel1(models.Model):
    STATUS_CHOICES = (
        ('0', "Non Aktif"),
        ('1', "Aktif"),
    )

    s_id_article = models.BigAutoField(primary_key=True)
    s_title = models.CharField(max_length=200, default='')
    s_description = models.TextField(max_length=200, default='')
    d_created_on = models.DateField(default=timezone.now)
    s_created_by = models.CharField(null=True, max_length=50)
    d_updated_on = models.DateField(null=True,blank=True)
    s_updated_by = models.CharField(null=True,blank=True, max_length=50)
    n_istatus = models.CharField(max_length=1, choices=STATUS_CHOICES, default='1')

    class Meta:
        db_table = 'tm_article1'   # ⬅️ Nama tabel manual
        verbose_name = 'Article 1'
        verbose_name_plural = 'Article 1'

    def __str__(self):
        return f"{self.s_title} ({self.get_n_istatus_display()})"

