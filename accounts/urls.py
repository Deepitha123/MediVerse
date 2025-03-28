from django.urls import path, include
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path('profile', views.profile, name='profile'),
    path('editprofile', views.editprofile, name='editprofile'),
    path('logout/', views.logout_view, name='logout'),
    path('wound/', views.wound_analysis, name='wound_analysis'),
    path('health_status/', views.health_status, name='health_status'),
    path('lifestyle_recommendations/', views.lifestyle_recommendations, name='lifestyle_recommendations'),
    path('about/', views.about, name='about'),
    path('mental_health/', views.mental_health, name='mental_health'),
    path('stress_analysis/', views.stress_analysis, name='stress_analysis'),
    path('sleep_analysis/', views.sleep_analysis, name='sleep_analysis'),




]