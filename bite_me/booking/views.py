# booking/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from datetime import datetime, timedelta

from .forms import RegistrationForm, ReservationForm
from .models import Reservation, Table

def index_view(request):
    """Render the homepage."""
    return render(request, 'booking/index.html')


def register_view(request):
    """Handle user registration."""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful! Welcome to Bite Me.")
            return redirect('index')
        else:
            messages.error(request, "There was an error with your registration. Please try again.")
    else:
        form = RegistrationForm()
    return render(request, 'booking/register.html', {'form': form})


def login_view(request):
    """Handle user login."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = AuthenticationForm()
    return render(request, 'booking/login.html', {'form': form})


def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('index')


@login_required
def menu_view(request):
    """Display the restaurant's menu."""
    from menu.models import Category
    categories = Category.objects.prefetch_related('items').all()
    return render(request, 'booking/menu.html', {'categories': categories})


@login_required
def create_reservation_view(request):
    """Allow users to create a reservation."""
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            if check_availability(reservation.date, reservation.time, reservation.guests):
                reservation.save()
                allocate_tables(reservation)
                messages.success(request, "Your reservation has been successfully created!")
                return redirect('my_bookings')
            else:
                messages.error(request, "Not enough tables available at the selected time.")
        else:
            messages.error(request, "Invalid form data. Please check your inputs.")
    else:
        form = ReservationForm()
    return render(request, 'booking/booking_form.html', {'form': form})


@login_required
def my_bookings_view(request):
    """Display user's current bookings."""
    reservations = request.user.reservations.filter(canceled=False).order_by('-date', '-time')
    return render(request, 'booking/bookings_list.html', {'reservations': reservations})


@login_required
def booking_detail_view(request, pk):
    """Display details of a specific reservation."""
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    return render(request, 'booking/booking_detail.html', {'reservation': reservation})


@login_required
def cancel_reservation_view(request, pk):
    """Allow users to cancel a reservation."""
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    if request.method == 'POST':
        reservation.canceled = True
        reservation.save()
        messages.success(request, "Reservation canceled successfully.")
        return redirect('my_bookings')
    return render(request, 'booking/cancellation.html', {'reservation': reservation})


# Helper functions

def check_availability(date, time, guests):
    """Check if there are enough tables available for the reservation."""
    tables = Table.objects.all().order_by('capacity')
    start_time = datetime.combine(date, time)
    end_time = start_time + timedelta(hours=2)  # Assuming a 2-hour reservation window

    existing_reservations = Reservation.objects.filter(
        date=date,
        canceled=False,
        time__gte=(start_time - timedelta(hours=2)).time(),
        time__lt=end_time.time()
    )

    occupied_capacity = sum(res.guests for res in existing_reservations)
    total_capacity = sum(t.capacity for t in tables)
    return (occupied_capacity + guests) <= total_capacity


def allocate_tables(reservation):
    """Allocate tables to meet the guest requirement."""
    tables = Table.objects.all().order_by('capacity')
    needed = reservation.guests
    chosen_tables = []
    for table in tables:
        if is_table_available(table, reservation.date, reservation.time):
            chosen_tables.append(table)
            needed -= table.capacity
            if needed <= 0:
                break
    reservation.tables.set(chosen_tables)
    reservation.save()


def is_table_available(table, date, time):
    """Check if a specific table is available at the given date and time."""
    start_time = datetime.combine(date, time)
    end_time = start_time + timedelta(hours=2)  # Assuming a 2-hour reservation window
    overlapping = table.reservations.filter(
        date=date,
        canceled=False,
        time__gte=(start_time - timedelta(hours=2)).time(),
        time__lt=end_time.time()
    )
    return not overlapping.exists()
