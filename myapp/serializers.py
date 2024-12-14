from rest_framework import serializers
from .models import Airline, Gate, CheckInCounter, Flight, Ticket
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]

class FlightSerializer(serializers.ModelSerializer):
    airline = serializers.StringRelatedField()
    gate = serializers.StringRelatedField()
    check_in_counter = serializers.StringRelatedField()
    class Meta:
        model = Flight
        fields = ['id', 'number', 'departure_time', 'arrival_time', 'boarding_time',
                  'destination', 'airline', 'gate', 'check_in_counter']

class TicketSerializer(serializers.ModelSerializer):
    flight = serializers.StringRelatedField()
    user = serializers.StringRelatedField()
    class Meta:
        model = Ticket
        fields = ['id', 'number', 'price', 'seat_number', 'flight', 'user', 'is_purchased']