# booking/urls.py

from django.urls import path
from .views import (
    index_view, register_view, login_view, logout_view,
    menu_view, create_reservation_view, my_bookings_view,
    booking_detail_view, cancel_reservation_view, dashboard_view,
    modify_reservation_view, profile_view, delete_account_view,
    admin_reservations_view, admin_update_reservation_status,
    admin_tables_view, edit_table_view, check_availability_view,
    contact_view
)

urlpatterns = [
    path('', index_view, name='index'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('menu/', menu_view, name='menu'),
    path('book/', create_reservation_view, name='book'),
    path('my-bookings/', my_bookings_view, name='my_bookings'),
    path('booking/<int:pk>/', booking_detail_view, name='booking_detail'),
    path('booking/<int:pk>/cancel/', cancel_reservation_view, name='cancel_reservation'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('booking/<int:pk>/modify/', modify_reservation_view, name='modify_reservation'),
    path('profile/', profile_view, name='profile'),
    path('delete-account/', delete_account_view, name='delete_account'),
    path('manage/reservations/', admin_reservations_view, name='admin_reservations'),
    path('manage/reservation/<int:pk>/status/', admin_update_reservation_status, name='admin_update_reservation_status'),
    path('manage/tables/', admin_tables_view, name='admin_tables'),
    path('manage/table/<int:pk>/edit/', edit_table_view, name='edit_table'),
    path('check-availability/', check_availability_view, name='check_availability'),
    path('contact/', contact_view, name='contact'),
]
