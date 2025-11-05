from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    points = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

class PickupRequest(models.Model):
    WASTE_TYPES = [
        ('wet', 'Wet Waste'),
        ('dry', 'Dry Waste'),
        ('recyclable', 'Recyclable'),
        ('hazardous', 'Hazardous'),
    ]
    
    QUANTITY_CHOICES = [
        ('small', 'Small (1-2 kg)'),
        ('medium', 'Medium (3-5 kg)'),
        ('large', 'Large (5+ kg)'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('picked', 'Picked Up'),
        ('completed', 'Completed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    waste_type = models.CharField(max_length=20, choices=WASTE_TYPES)
    quantity = models.CharField(max_length=10, choices=QUANTITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    points_awarded = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.waste_type} - {self.created_at.strftime('%Y-%m-%d')}"

# Signal to create user profile when user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)