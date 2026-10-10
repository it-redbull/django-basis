from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('wachtwoord-wijzigen/', views.change_password_view, name='change_password'),
    path('pending/', views.pending, name='pending'),

]

