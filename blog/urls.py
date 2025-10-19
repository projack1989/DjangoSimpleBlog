from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import IndexView

urlpatterns = [
    path('adminRoot/', admin.site.urls),
    path('', IndexView.as_view(),name="index"),
    path('testing/', IndexView.as_view(),name="testing"),
    path('about/', include(('about.urls', 'about'), namespace='about')),
    path('contactPage/', include('contact.urls')),
    path('singlePost/', include('singlepost.urls')),
    path('login/', include('adminpanel.urls')),
]

# Tambahkan ini di bawah sekali untuk upload image ke folder MEDIA. Cek konfigurasi di settings.py:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)