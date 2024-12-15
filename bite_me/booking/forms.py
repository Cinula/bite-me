# booking/forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Reservation
from datetime import datetime, timedelta

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Update password field widgets
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email


class ReservationForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control form-control-lg',
                'min': datetime.now().date().isoformat(),
                'max': (datetime.now() + timedelta(days=30)).date().isoformat(),  # Allow bookings up to 30 days ahead
            }
        ),
        label='Date'
    )
    
    time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={
                'type': 'time',
                'class': 'form-control form-control-lg',
                'min': '11:00',
                'max': '22:00'
            }
        ),
        label='Time'
    )
    
    guests = forms.IntegerField(
        min_value=1,
        max_value=20,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Number of guests'
            }
        ),
        label='Number of Guests'
    )

    class Meta:
        model = Reservation
        fields = ['date', 'time', 'guests']

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date < datetime.now().date():
            raise forms.ValidationError("You cannot make reservations for past dates.")
        if date > datetime.now().date() + timedelta(days=30):
            raise forms.ValidationError("Reservations can only be made up to 30 days in advance.")
        return date

    def clean_time(self):
        time = self.cleaned_data.get('time')
        if time:
            if time.hour < 11 or time.hour >= 22:
                raise forms.ValidationError("Reservations are only accepted between 11:00 AM and 10:00 PM.")
        return time

class UserProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    current_password = forms.CharField(
        widget=forms.PasswordInput(),
        required=False,
        help_text='Enter current password to confirm changes'
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(),
        required=False,
        help_text='Leave blank to keep current password'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(),
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get('current_password')
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and not current_password:
            raise forms.ValidationError('Current password is required to set a new password')

        if new_password != confirm_password:
            raise forms.ValidationError('New passwords do not match')

        return cleaned_data
