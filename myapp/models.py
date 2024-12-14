from django.db import models
from django.contrib.auth.models import User

class Airline(models.Model):
    name = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.name

class Gate(models.Model):
    number = models.CharField(max_length=20)
    status = models.CharField(max_length=40, default="Available")
    def __str__(self):
        return f"Gate {self.number} - {self.status}"


class CheckInCounter(models.Model):
    number = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=40, default="Available")
    def __str__(self):
        return f"Check-In Counter {self.number} - {self.status}"


class Flight(models.Model):
    number = models.CharField(max_length=45)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    airline = models.ForeignKey('Airline', on_delete=models.CASCADE, related_name='flights')
    boarding_time = models.DateTimeField()
    destination = models.CharField(max_length=250)
    gate = models.ForeignKey(Gate, on_delete=models.CASCADE, related_name='flights')
    check_in_counter = models.ForeignKey('CheckInCounter', on_delete=models.SET_NULL, null=True, blank=True, related_name='flights')

    def __str__(self):
        return f"Flight {self.number} to {self.destination}"

    def get_duration(self):
        return self.arrival_time - self.departure_time

class Ticket(models.Model):
    number = models.CharField(max_length=25, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seat_number = models.CharField(max_length=10)
    flight = models.ForeignKey('Flight', on_delete=models.CASCADE, related_name='tickets')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets', null=True, blank=True)
    is_purchased = models.BooleanField(default=False)

    def __str__(self):
        status = "Purchased" if self.is_purchased else "Available"
        return f"Ticket {self.number} for Seat {self.seat_number} - Flight {self.flight.number} ({status})"



