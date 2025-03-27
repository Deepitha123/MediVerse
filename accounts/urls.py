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




]