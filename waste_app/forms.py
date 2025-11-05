from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
            'placeholder': 'Enter your phone number'
        })
    )
    address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 3,
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
            'placeholder': 'Enter your address'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'phone', 'address', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['phone', 'address']:
                field.widget.attrs.update({
                    'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
                })

    def save(self, commit=True):
        # Save the user first
        user = super().save(commit=commit)
        
        # The signal should have created the profile automatically
        # Just update the phone and address if they exist
        if hasattr(user, 'userprofile'):
            profile = user.userprofile
            profile.phone = self.cleaned_data.get('phone', '')
            profile.address = self.cleaned_data.get('address', '')
            profile.save()
        
        return user