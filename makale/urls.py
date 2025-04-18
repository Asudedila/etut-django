from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.anasayfa, name='anasayfa'),
    path('etut/ekle/', views.etut_ekle, name='etut_ekle'),
    path('etut/rezerve/<int:id>/', views.etut_rezerve, name='etut_rezerve'),
    path('etut/iptal/<int:id>/', views.etut_iptal, name='etut_iptal'),
    path("kayit/", views.kayit, name="kayit"),


]
