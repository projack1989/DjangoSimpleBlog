from django.urls import path
from . import views
from about.views import IndexView as BlogIndexView

app_name = 'about'

urlpatterns = [
    path('about/', views.about, name='index'),
    #path('about/', BlogIndexView.as_view(), name='about_index'),

]