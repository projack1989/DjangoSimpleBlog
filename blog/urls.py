from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
#from .import views
from .views import IndexView
from about.views import IndexView as BlogIndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(),name="index"),
    path('testing/', IndexView.as_view(),name="testing"),
    path('about/', BlogIndexView.as_view(),name="about"),
    #path('about/', include('about.urls'),name="about"), # Tambahkan ini
    path('frontend/', include('adminpanel.urls')),
    path('contactPage/', include('contact.urls')),
    path('singlePost/', include('singlepost.urls')),
]

# Tambahkan ini di bawah sekali untuk upload image ke folder MEDIA. Cek konfigurasi di settings.py:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)