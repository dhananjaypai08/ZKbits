from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.startup, name='startup'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('adminlogin/', views.adminlogin, name='adminlogin'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout, name='logout'),
    path('adminhome/', views.adminhome, name='adminhome'),
    path('adminview/', views.adminview, name='adminview'),
    path('adminadd/', views.adminadd, name='adminadd'),
    path('adminupdate/', views.adminupdate, name='adminupdate'),
    path('admindelete/', views.admindelete, name='admindelete'),
    path('userview/', views.userview, name='userview'),
    path('mail/', views.mail, name='mail'),
]
