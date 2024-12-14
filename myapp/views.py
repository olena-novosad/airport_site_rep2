from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages

from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.renderers import TemplateHTMLRenderer

from .models import Airline, Gate, CheckInCounter, Flight, Ticket
from .serializers import FlightSerializer, TicketSerializer, UserSerializer
from .forms import FlightForm, TicketForm, UserRegisterForm

from django.contrib.auth.models import User

@api_view(['GET'])
def flight_list(request):
    order = request.GET.get('order')
    if order == 'asc':
        flights = Flight.objects.all().order_by('departure_time')
    elif order == 'desc':
        flights = Flight.objects.all().order_by('-departure_time')
    else:
        flights = Flight.objects.all()
    return render(request, 'myapp/flight_list.html', {
        'flights': flights,
        'order': order
    })

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def add_flight(request):
    if not request.user.is_superuser:
        messages.error(request, "You are not authorized to add flights.")
        return HttpResponseForbidden("You are not authorized to add flights.")

    if request.method == 'POST':
        form = FlightForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Flight added successfully!")
            return redirect('flight_list')
    else:
        form = FlightForm()

    return render(request, 'myapp/flight_form.html', {'form': form})


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def delete_flight(request, flight_id):
    flight = get_object_or_404(Flight, pk=flight_id)
    if request.method == 'POST':
        flight.delete()
        return redirect('flight_list')
    return render(request, 'myapp/flight_confirm_delete.html', {'flight': flight})

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def add_ticket(request, flight_id):

    flight = get_object_or_404(Flight, pk=flight_id)

    if not request.user.is_superuser:
        messages.error(request, "You are not authorized to add tickets.")
        return HttpResponseForbidden("You are not authorized to add tickets.")

    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.flight = flight
            ticket.save()
            messages.success(request, "Ticket added successfully!")
            return redirect('flight_detail', flight_id=flight_id)
    else:
        form = TicketForm(initial={'flight': flight})

    return render(request, 'myapp/ticket_form.html', {'form': form, 'flight': flight})

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def edit_ticket(request, ticket_id):

    ticket = get_object_or_404(Ticket, pk=ticket_id)
    flight = ticket.flight

    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('flight_detail', flight_id=flight.id)
    else:
        form = TicketForm(instance=ticket)

    return render(request, 'myapp/ticket_form.html', {'form': form, 'ticket': ticket, 'flight': flight})


@api_view(['GET'])
def flight_detail_with_tickets(request, flight_id):

    flight = get_object_or_404(Flight, pk=flight_id)
    order = request.GET.get('order', None)

    tickets_query = Ticket.objects.filter(flight=flight, is_purchased=False)
    if not request.user.is_authenticated:
        return redirect('login')

    if order == 'asc':
        tickets = tickets_query.order_by('price')
    elif order == 'desc':
        tickets = tickets_query.order_by('-price')
    else:
        tickets = tickets_query

    return render(request, 'myapp/flight_detail.html', {
        'flight': flight,
        'tickets': tickets,
        'order': order,
    })

from django.contrib.auth.decorators import login_required

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def buy_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)

    ticket.is_purchased = True
    ticket.user = request.user
    ticket.save()

    return redirect('flight_detail', flight_id=ticket.flight.id)

@api_view(['GET'])
def check_in_counters_list(request):
    counters = CheckInCounter.objects.all()
    return render(request, 'myapp/check_in_counters_list.html', {'counters': counters})

@api_view(['GET'])
def gates_list(request):
    gates = Gate.objects.all()
    return render(request, 'myapp/gates_list.html', {'gates': gates})


def registerPage(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegisterForm()
    return render(request, 'myapp/register.html', {'form': form})


@login_required
def logoutPage(request):
    logout(request)
    return redirect('main_page')

@login_required
def return_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    if ticket.is_purchased and ticket.user == request.user:
        ticket.is_purchased = False
        ticket.user = None
        ticket.save()
        messages.success(request, "Ticket has been successfully returned.")
    else:
        messages.error(request, "You are not authorized to return this ticket.")

    return redirect('user_detail')

class UserDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "myapp/user_profile.html"

    def get(self, request):
        if request.user.is_authenticated:
            user = get_object_or_404(User, username=request.user.username)
            tickets = Ticket.objects.filter(user=user)
            serializer = UserSerializer(user)
            return Response({
                "serializer": serializer,
                "user": user,
                "tickets": tickets
            })
        else:
            return redirect('login')


def main_page(request):
    context = {
        'airport_name': 'Lviv International Airport',
        'current_year': 2024,
    }
    return render(request, 'myapp/main.html', context)