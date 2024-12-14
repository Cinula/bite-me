# booking/forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Reservation

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ReservationForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.SelectDateWidget(attrs={'class': 'form-control'}),
        label='Date'
    )
    time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        label='Time'
    )
    guests = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label='Number of Guests'
    )

    class Meta:
        model = Reservation
        fields = ['date', 'time', 'guests']
