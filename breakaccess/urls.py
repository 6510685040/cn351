from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('home/<int:user_id>/', views.home, name='home'),
    path("register/", views.register, name="register"),
    path('logout/', views.logout_view, name='logout'),
]
