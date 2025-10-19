from django.db import models
import uuid

# Create your models here.

class TmUser(models.Model):
    s_id_user       = models.CharField(primary_key=True, max_length=100,default=uuid.uuid4)
    s_first_name    = models.CharField(max_length=50)
    s_last_name     = models.CharField(max_length=50)
    s_email         = models.EmailField(max_length=100, unique=True)
    s_password      = models.CharField(null=False,blank=False, max_length=255)
    s_status        = models.CharField(max_length=20, default='1')
    d_created_on    = models.DateTimeField(auto_now_add=True)
    s_created_by    = models.CharField(max_length=50,default=s_email)
    d_updated_on    = models.DateTimeField(null=True, blank=True)
    s_updated_by    = models.CharField(max_length=50)
    class Meta:
        db_table = 'tm_user'