from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('home/<int:user_id>/', views.home, name='home'),
    path("register/", views.register, name="register"),
    path('logout/', views.logout_view, name='logout'),
    path('admin-dashboard', views.admin_dashboard_js_controlled, name='admin_dashboard_js_controlled'),
    path('delete-user/<int:user_id>/', views.insecure_delete_user_js_controlled, name='insecure_delete_user_js_controlled'),
]
