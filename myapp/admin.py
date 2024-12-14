
from django.contrib import admin
from .models import Airline, Gate, CheckInCounter, Flight, Ticket

admin.site.register(Airline)
admin.site.register(Gate)
admin.site.register(CheckInCounter)

class FlightAdmin(admin.ModelAdmin):
    list_display = ('number', 'airline', 'destination', 'departure_time', 'arrival_time', 'gate', 'check_in_counter')
    list_filter = ('airline', 'destination', 'gate', 'check_in_counter')

admin.site.register(Flight, FlightAdmin)

class TicketAdmin(admin.ModelAdmin):
    list_display = ('number', 'seat_number', 'price', 'flight', 'user', 'is_purchased')
    list_filter = ('is_purchased', 'flight')
    search_fields = ('number', 'user__username', 'flight__number')

admin.site.register(Ticket, TicketAdmin)
