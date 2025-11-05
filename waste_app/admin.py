from django.contrib import admin
from .models import UserProfile, PickupRequest

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'points', 'address']

@admin.register(PickupRequest)
class PickupRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'waste_type', 'quantity', 'status', 'created_at']
    list_filter = ['status', 'waste_type']