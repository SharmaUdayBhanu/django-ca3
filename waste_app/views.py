from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User 
from django.views.decorators.http import require_POST
from .forms import CustomUserCreationForm
from .models import UserProfile, PickupRequest

# Check if user is admin
def is_admin(user):
    return user.is_authenticated and user.is_staff

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@require_POST
def custom_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')

@login_required
def dashboard(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user, phone='', address='')
    
    pickup_requests = PickupRequest.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'dashboard.html', {
        'profile': profile,
        'pickup_requests': pickup_requests
    })

@login_required
def request_pickup(request):
    if request.method == 'POST':
        waste_type = request.POST.get('waste_type')
        quantity = request.POST.get('quantity')
        
        if waste_type and quantity:
            pickup = PickupRequest.objects.create(
                user=request.user,
                waste_type=waste_type,
                quantity=quantity,
                status='pending'
            )
            messages.success(request, 'Pickup request submitted successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please select both waste type and quantity.')
    
    return render(request, 'request_pickup.html')

# Admin Views
def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, 'Admin login successful!')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid admin credentials or insufficient permissions.')
    
    return render(request, 'admin_login.html')

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    # Admin statistics
    total_users = User.objects.count()
    total_pickups = PickupRequest.objects.count()
    pending_pickups = PickupRequest.objects.filter(status='pending').count()
    completed_pickups = PickupRequest.objects.filter(status='completed').count()
    total_points = sum(profile.points for profile in UserProfile.objects.all())
    
    # Recent pickups
    recent_pickups = PickupRequest.objects.select_related('user').order_by('-created_at')[:10]
    
    # Recent users
    recent_users = User.objects.select_related('userprofile').order_by('-date_joined')[:5]
    
    context = {
        'stats': {
            'total_users': total_users,
            'total_pickups': total_pickups,
            'pending_pickups': pending_pickups,
            'completed_pickups': completed_pickups,
            'total_points': total_points,
        },
        'recent_pickups': recent_pickups,
        'recent_users': recent_users,
    }
    return render(request, 'admin_dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def admin_users(request):
    users = User.objects.select_related('userprofile').all()
    return render(request, 'admin_users.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def admin_pickups(request):
    status_filter = request.GET.get('status', '')
    if status_filter:
        pickups = PickupRequest.objects.select_related('user').filter(status=status_filter).order_by('-created_at')
    else:
        pickups = PickupRequest.objects.select_related('user').all().order_by('-created_at')
    
    return render(request, 'admin_pickups.html', {
        'pickups': pickups,
        'current_status': status_filter
    })

@login_required
@user_passes_test(is_admin)
def update_pickup_status(request, pickup_id):
    if request.method == 'POST':
        pickup = PickupRequest.objects.get(id=pickup_id)
        new_status = request.POST.get('status')
        pickup.status = new_status
        
        # Award points if completing and not already awarded
        if new_status == 'completed' and not pickup.points_awarded:
            points = 10 if pickup.waste_type == 'recyclable' else 5
            profile = pickup.user.userprofile
            profile.points += points
            profile.save()
            pickup.points_awarded = True
        
        pickup.save()
        messages.success(request, f'Pickup status updated to {new_status}')
    
    return redirect('admin_pickups')