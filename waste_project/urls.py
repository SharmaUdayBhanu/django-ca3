from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Django built-in admin
    path('', include('waste_app.urls')),  # Your app URLs (includes login/logout)
]