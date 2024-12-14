from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.decorators import user_passes_test

from .forms import RegistrationForm, ReservationForm
from .models import Reservation, Table

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegistrationForm()
    return render(request, 'booking/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'booking/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

def index_view(request):
    return render(request, 'booking/index.html')

@login_required
def menu_view(request):
    from menu.models import Category
    categories = Category.objects.prefetch_related('items').all()
    return render(request, 'booking/menu.html', {'categories': categories})

@login_required
def create_reservation_view(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user

            if check_availability(reservation.date, reservation.time, reservation.guests):
                reservation.save()
                allocate_tables(reservation)
                messages.success(request, "Reservation created successfully!")
                return redirect('my_bookings')
            else:
                messages.error(request, "Not enough tables available at the selected time.")
    else:
        form = ReservationForm()
    return render(request, 'booking/booking_form.html', {'form': form})

@login_required
def my_bookings_view(request):
    reservations = request.user.reservations.filter(canceled=False).order_by('-date', '-time')
    return render(request, 'booking/bookings_list.html', {'reservations': reservations})

@login_required
def booking_detail_view(request, pk):
    reservation = Reservation.objects.get(pk=pk, user=request.user)
    return render(request, 'booking/booking_detail.html', {'reservation': reservation})

@login_required
def cancel_reservation_view(request, pk):
    reservation = Reservation.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        reservation.canceled = True
        reservation.save()
        messages.success(request, "Reservation canceled.")
        return redirect('my_bookings')
    return render(request, 'booking/cancellation.html', {'reservation': reservation})


# Helper functions
def check_availability(date, time, guests):
    tables = Table.objects.all().order_by('capacity')
    start_time = datetime.combine(date, time)
    end_time = start_time + timedelta(hours=2)

    existing_reservations = Reservation.objects.filter(
        date=date, canceled=False,
        time__gte=(start_time - timedelta(hours=2)).time(),
        time__lt=end_time.time()
    )

    occupied_capacity = 0
    for res in existing_reservations:
        occupied_capacity += res.guests

    total_capacity = sum([t.capacity for t in tables])
    return (occupied_capacity + guests) <= total_capacity

def allocate_tables(reservation):
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
    start_time = datetime.combine(date, time)
    end_time = start_time + timedelta(hours=2)
    overlapping = table.reservations.filter(
        date=date, canceled=False,
        time__gte=(start_time - timedelta(hours=2)).time(),
        time__lt=end_time.time()
    )
    return not overlapping.exists()

def is_staff(user):
    return user.is_staff or user.is_superuser

@user_passes_test(is_staff)
def manage_bookings_view(request):
    all_reservations = Reservation.objects.filter(canceled=False).order_by('-date', '-time')
    return render(request, 'booking/manage_bookings.html', {'all_reservations': all_reservations})