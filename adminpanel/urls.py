from django.urls import path
from . import views

app_name = 'adminpanel'

urlpatterns = [
    path('', views.index, name='login'),
    path('blank-page/', views.blank_page, name='blank-page'),
    path('master-form/', views.master_form, name='master-form'),
    path('admin-login/', views.index, name='admin-login'),
]