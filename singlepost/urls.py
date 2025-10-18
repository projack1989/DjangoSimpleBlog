from django.urls import path
from . import views

app_name = 'singlepost'

urlpatterns = [
    path('index/', views.index, name='index'),

]