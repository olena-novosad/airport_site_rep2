from django.urls import path
from .views import flight_list, add_flight, delete_flight, flight_detail_with_tickets, add_ticket, edit_ticket, buy_ticket, check_in_counters_list, gates_list, registerPage, logoutPage, UserDetail, return_ticket, main_page
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('flights/', flight_list, name='flight_list'),  # Список всіх рейсів
    path('flights/add/', add_flight, name='add_flight'),  # Додавання рейсу
    path('flights/<int:flight_id>/delete/', delete_flight, name='delete_flight'),  # Видалення рейсу
    path('flights/<int:flight_id>/', flight_detail_with_tickets, name='flight_detail'),  # Деталі рейсу
    path('flights/<int:flight_id>/add_ticket/', add_ticket, name='add_ticket'),  # Додавання квитка
    path('tickets/<int:ticket_id>/edit/', edit_ticket, name='edit_ticket'),  # Редагування квитка
    path('tickets/<int:ticket_id>/buy/', buy_ticket, name='buy_ticket'),
    path('check_in_counters/', check_in_counters_list, name='check_in_counters_list'),  # Список стійок реєстрації
    path('gates/', gates_list, name='gates_list'),
    path('login/', auth_views.LoginView.as_view(template_name='myapp/login.html'), name='login'),
    path('register/', registerPage, name='register'),
    path('logout/', logoutPage, name='logout'),
    path('flights/', flight_list, name='flight_list'),
    path('add_flight/', add_flight, name='add_flight'),
    path('user/detail/', UserDetail.as_view(), name='user_detail'),
    path('tickets/<int:ticket_id>/return/', return_ticket, name='return_ticket'),
    path('', main_page, name='main_page'),
]