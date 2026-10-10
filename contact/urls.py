from django.urls import path

from . import views

urlpatterns = [
    path('proefrit/', views.proefrit, name='proefrit'),
    path('', views.contact, name='contact'),
    path('proefritpagina/', views.proefritpage, name='proefritpage'),
]