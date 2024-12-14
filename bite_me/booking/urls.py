from django.urls import path
from .views import (
    index_view, register_view, login_view, logout_view,
    menu_view, create_reservation_view, my_bookings_view,
    booking_detail_view, cancel_reservation_view, manage_bookings_view
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
    path('manage-bookings/', manage_bookings_view, name='manage_bookings'),
    
]
