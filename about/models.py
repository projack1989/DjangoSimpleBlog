from django.db import models
from django.utils import timezone
    
class About(models.Model):
    STATUS_CHOICES = (
        ('0', "Non Aktif"),
        ('1', "Aktif"),
    )

    s_id_about = models.BigAutoField(primary_key=True)
    s_title = models.CharField(max_length=200, default='')
    s_description = models.TextField(max_length=200, default='')
    d_created_on = models.DateField(default=timezone.now)
    s_created_by = models.CharField(null=True, max_length=50)
    d_updated_on = models.DateField(null=True,blank=True)
    s_updated_by = models.CharField(null=True,blank=True, max_length=50)
    n_istatus = models.CharField(max_length=1, choices=STATUS_CHOICES, default='1')

    class Meta:
        db_table = 'tm_about'   # ⬅️ Nama tabel manual
        verbose_name = 'About'
        verbose_name_plural = 'About'

    def __str__(self):
        return f"{self.s_title} ({self.get_n_istatus_display()})"

