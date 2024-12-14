from django import forms
from .models import Airline, Gate, CheckInCounter, Flight, Ticket
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Поле email як обов'язкове

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'first_name',
            'last_name',
        ]

class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = ['number', 'departure_time', 'arrival_time', 'airline', 'boarding_time', 'destination', 'gate', 'check_in_counter']
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'departure_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'arrival_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'boarding_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'airline': forms.Select(attrs={'class': 'form-control'}),
            'destination': forms.TextInput(attrs={'class': 'form-control'}),
            'gate': forms.Select(attrs={'class': 'form-control'}),
            'check_in_counter': forms.Select(attrs={'class': 'form-control'}),
        }

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['number', 'price', 'seat_number']
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'seat_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
