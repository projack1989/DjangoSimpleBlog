from django.urls import path
from . import views

app_name = 'adminpanel'

urlpatterns = [
    path('', views.index, name='index'),
    path('blank-page/', views.blank_page, name='blank-page'),
    path('master-form/', views.master_form, name='master-form'),
    path('admin-login/', views.index, name='admin-login'),
    path('register/', views.register, name='register'),
    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('logout/', views.logout, name='logout'),
]