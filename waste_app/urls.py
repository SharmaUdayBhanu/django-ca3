from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Public routes
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),  # Your custom logout
    path('dashboard/', views.dashboard, name='dashboard'),
    path('request-pickup/', views.request_pickup, name='request_pickup'),
    
    # Custom Admin routes - Using 'portal/' prefix to avoid conflict with Django admin
    path('portal/login/', views.admin_login, name='admin_login'),
    path('portal/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('portal/users/', views.admin_users, name='admin_users'),
    path('portal/pickups/', views.admin_pickups, name='admin_pickups'),
    path('portal/pickups/<int:pickup_id>/update/', views.update_pickup_status, name='update_pickup_status'),
]