from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Flight, Airline, Gate, Ticket
from datetime import datetime, timedelta
from django.utils.timezone import make_aware

class AddFlightTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.superuser = User.objects.create_superuser(username='admin', password='adminpassword')
        cls.regular_user = User.objects.create_user(username='testuser', password='testpassword')
        cls.airline = Airline.objects.create(name="Test Airline")
        cls.gate = Gate.objects.create(number="A1", status="Available")

    def test_add_flight_as_superuser(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.post(reverse('add_flight'), {
            'number': 'FL456',
            'departure_time': '2024-12-25 14:00:00',
            'arrival_time': '2024-12-25 16:00:00',
            'airline': self.airline.id,
            'boarding_time': '2024-12-25 13:30:00',
            'destination': 'Lviv',
            'gate': self.gate.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Flight.objects.filter(number='FL456').exists())  # Рейс має існувати
        flight = Flight.objects.get(number='FL456')
        self.assertEqual(flight.destination, 'Lviv')
        self.assertEqual(flight.airline, self.airline)
        self.assertEqual(flight.gate, self.gate)

    def test_add_flight_as_regular_user(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(reverse('add_flight'), {
            'number': 'FL456',
            'departure_time': '2024-12-25 14:00:00',
            'arrival_time': '2024-12-25 16:00:00',
            'airline': self.airline.id,
            'boarding_time': '2024-12-25 13:30:00',
            'destination': 'Lviv',
            'gate': self.gate.id
        })

        self.assertEqual(response.status_code, 403)  # Код 403 означає заборону доступу
        self.assertFalse(Flight.objects.filter(number='FL456').exists())  # Рейс не повинен створитися

class AddTicketTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.superuser = User.objects.create_superuser(username='admin', password='adminpassword')
        cls.regular_user = User.objects.create_user(username='testuser', password='testpassword')
        cls.airline = Airline.objects.create(name="Test Airline")
        cls.gate = Gate.objects.create(number="A1", status="Available")
        cls.flight = Flight.objects.create(
            number="FL123",
            departure_time="2024-12-25 10:00:00",
            arrival_time="2024-12-25 12:00:00",
            airline=cls.airline,
            boarding_time="2024-12-25 09:30:00",
            destination="Kyiv",
            gate=cls.gate
        )

    def test_add_ticket_as_superuser(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.post(reverse('add_ticket', args=[self.flight.id]), {
            'number': 'T123',
            'price': 100.00,
            'seat_number': '1A',
        })
        self.assertIn(response.status_code, [200, 302])  # Перевіряємо або успішне завантаження, або перенаправлення
        self.assertTrue(Ticket.objects.filter(number='T123').exists())  # Квиток має існувати
        ticket = Ticket.objects.get(number='T123')
        self.assertEqual(ticket.flight, self.flight)

    def test_add_ticket_as_regular_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('add_ticket', args=[self.flight.id]), {
            'number': 'T123',
            'price': 100.00,
            'seat_number': '1A',
        })

        self.assertEqual(response.status_code, 403)  # Код 403 означає заборону доступу
        self.assertFalse(Ticket.objects.filter(number='T123').exists())  # Квиток не повинен створитися


class FlightModelTestCase(TestCase):

    def setUp(self):
        self.flight_normal = Flight(
            number="FL123",
            departure_time=make_aware(datetime(2024, 12, 25, 10, 0)),
            arrival_time=make_aware(datetime(2024, 12, 25, 12, 30)),  # 2 години 30 хвилин
            boarding_time=make_aware(datetime(2024, 12, 25, 9, 30)),
            destination="Kyiv"
        )

        self.flight_next_day_arrival = Flight(
            number="FL126",
            departure_time=make_aware(datetime(2024, 12, 25, 23, 0)),
            arrival_time=make_aware(datetime(2024, 12, 26, 1, 0)),  # 2 години (перехід через добу)
            boarding_time=make_aware(datetime(2024, 12, 25, 22, 30)),
            destination="Kyiv"
        )

    def test_get_duration_positive(self):
        duration = self.flight_normal.get_duration()
        expected_duration = timedelta(hours=2, minutes=30)  # Очікувана тривалість 2 години 30 хвилин
        self.assertEqual(duration, expected_duration, "Duration calculation for normal flight is incorrect")

    def test_get_next_day_arrival(self):
        duration = self.flight_next_day_arrival.get_duration()
        expected_duration = timedelta(hours=2)
        self.assertEqual(duration, expected_duration, "Duration for next-day arrival flight is incorrect")
