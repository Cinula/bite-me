# booking/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from datetime import datetime, timedelta
from django.http import JsonResponse

from .forms import RegistrationForm, ReservationForm, UserProfileForm
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
            return redirect('dashboard')
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


def menu_view(request):
    """Display the restaurant's menu."""
    from menu.models import Category
    categories = Category.objects.prefetch_related('items').all()
    return render(request, 'menu/menu.html', {'categories': categories})


@login_required
def create_reservation_view(request):
    """Allow users to create a reservation."""
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            
            # Get selected tables
            selected_table_ids = request.POST.getlist('selected_tables')
            selected_tables = Table.objects.filter(id__in=selected_table_ids)
            
            # Calculate total capacity of selected tables
            total_capacity = sum(table.capacity for table in selected_tables)
            
            if total_capacity >= reservation.guests:
                # Check if all selected tables are available
                all_tables_available = all(
                    is_table_available(table, reservation.date, reservation.time)
                    for table in selected_tables
                )
                
                if all_tables_available:
                    reservation.save()
                    reservation.tables.set(selected_tables)
                    messages.success(request, "Your reservation has been successfully created!")
                    return redirect('my_bookings')
                else:
                    messages.error(request, "Some selected tables are not available. Please choose different tables.")
            else:
                messages.error(request, "Selected tables don't have enough capacity for your party size.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ReservationForm()
    
    # Get available tables for the layout
    tables = Table.objects.all().order_by('number')
    occupied_tables = Table.objects.filter(
        reservations__date=datetime.now().date(),
        reservations__canceled=False
    )
    
    context = {
        'form': form,
        'tables': tables,
        'occupied_tables': occupied_tables,
        'today': datetime.now().date()
    }
    return render(request, 'booking/booking_form.html', context)


@login_required
def my_bookings_view(request):
    """Display user's current bookings."""
    reservations = request.user.reservations.all().order_by('-date', '-time')
    context = {
        'reservations': reservations,
        'today': datetime.now().date()
    }
    return render(request, 'booking/bookings_list.html', context)


@login_required
def booking_detail_view(request, pk):
    """Display details of a specific reservation."""
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    context = {
        'reservation': reservation,
        'today': datetime.now().date()
    }
    return render(request, 'booking/booking_detail.html', context)


@login_required
def cancel_reservation_view(request, pk):
    """Allow users to cancel a reservation."""
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    
    # Don't allow cancellation of past reservations
    if reservation.date < datetime.now().date():
        messages.error(request, "Past reservations cannot be cancelled.")
        return redirect('booking_detail', pk=pk)
    
    if request.method == 'POST':
        reservation.canceled = True
        reservation.save()
        messages.success(request, "Your reservation has been cancelled successfully.")
        return redirect('my_bookings')
    
    # If it's not a POST request, redirect back to the detail page
    return redirect('booking_detail', pk=pk)


@login_required
def dashboard_view(request):
    """User dashboard showing reservations and account info."""
    # Get user's upcoming reservations
    upcoming_reservations = request.user.reservations.filter(
        date__gte=datetime.now().date(),
        canceled=False
    ).order_by('date', 'time')[:5]
    
    # Get user's past reservations
    past_reservations = request.user.reservations.filter(
        date__lt=datetime.now().date(),
        canceled=False
    ).order_by('-date', '-time')[:5]
    
    context = {
        'upcoming_reservations': upcoming_reservations,
        'past_reservations': past_reservations,
        'user': request.user,
    }
    return render(request, 'booking/dashboard.html', context)


@login_required
def modify_reservation_view(request, pk):
    """Allow users to modify their reservation."""
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    
    # Don't allow modification of past or cancelled reservations
    if reservation.date < datetime.now().date() or reservation.canceled:
        messages.error(request, "This reservation cannot be modified.")
        return redirect('booking_detail', pk=pk)
    
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            new_reservation = form.save(commit=False)
            if check_availability(new_reservation.date, new_reservation.time, new_reservation.guests):
                # Clear existing table assignments
                reservation.tables.clear()
                new_reservation.save()
                # Allocate new tables
                allocate_tables(new_reservation)
                messages.success(request, "Reservation updated successfully!")
                return redirect('booking_detail', pk=pk)
            else:
                messages.error(request, "Not enough tables available at the selected time.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ReservationForm(instance=reservation)
    
    context = {
        'form': form,
        'reservation': reservation,
    }
    return render(request, 'booking/modify_reservation.html', context)


@login_required
def profile_view(request):
    """Handle user profile management."""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            current_password = form.cleaned_data.get('current_password')
            new_password = form.cleaned_data.get('new_password')
            
            # First save the basic profile changes
            user = form.save(commit=False)
            
            # Handle password change if requested
            if new_password:
                if not current_password:
                    messages.error(request, 'Current password is required to change password.')
                    return redirect('profile')
                
                if not request.user.check_password(current_password):
                    messages.error(request, 'Current password is incorrect.')
                    return redirect('profile')
                
                # Set and save the new password
                user.set_password(new_password)
                user.save()
                
                messages.success(request, 'Profile and password updated successfully. Please login again.')
                logout(request)
                return redirect('login')
            else:
                # Save profile changes without password change
                user.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'booking/profile.html', {'form': form})


@login_required
def delete_account_view(request):
    """Handle account deletion."""
    if request.method == 'POST':
        password = request.POST.get('password')
        user = request.user
        
        # Verify password
        if user.check_password(password):
            # Delete the user account
            user.delete()
            messages.success(request, 'Your account has been successfully deleted.')
            return redirect('index')
        else:
            messages.error(request, 'Incorrect password. Account deletion cancelled.')
            return redirect('profile')
    
    return redirect('profile')


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


@user_passes_test(lambda u: u.is_staff)
def admin_reservations_view(request):
    """Admin interface for managing reservations."""
    # Get filter parameters
    date_filter = request.GET.get('date')
    status_filter = request.GET.get('status')
    search_query = request.GET.get('search')

    # Base queryset
    reservations = Reservation.objects.select_related('user').all()

    # Apply filters
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            reservations = reservations.filter(date=filter_date)
        except ValueError:
            pass

    if status_filter:
        if status_filter == 'upcoming':
            reservations = reservations.filter(
                date__gte=datetime.now().date(),
                canceled=False
            )
        elif status_filter == 'past':
            reservations = reservations.filter(
                date__lt=datetime.now().date(),
                canceled=False
            )
        elif status_filter == 'canceled':
            reservations = reservations.filter(canceled=True)

    if search_query:
        reservations = reservations.filter(
            user__username__icontains=search_query
        )

    # Order by date and time
    reservations = reservations.order_by('-date', '-time')

    context = {
        'reservations': reservations,
        'today': datetime.now().date(),
        'date_filter': date_filter,
        'status_filter': status_filter,
        'search_query': search_query
    }
    return render(request, 'booking/admin/reservations.html', context)

@user_passes_test(lambda u: u.is_staff)
def admin_update_reservation_status(request, pk):
    """Handle reservation status updates by admin."""
    if request.method == 'POST':
        reservation = get_object_or_404(Reservation, pk=pk)
        action = request.POST.get('action')
        
        if action == 'cancel':
            reservation.canceled = True
            reservation.save()
            messages.success(request, f'Reservation #{pk} has been cancelled.')
        elif action == 'restore':
            reservation.canceled = False
            reservation.save()
            messages.success(request, f'Reservation #{pk} has been restored.')
    
    return redirect('admin_reservations')

@user_passes_test(lambda u: u.is_staff)
def admin_tables_view(request):
    """Admin interface for managing restaurant tables."""
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add':
            number = request.POST.get('number')
            capacity = request.POST.get('capacity')
            try:
                Table.objects.create(number=number, capacity=capacity)
                messages.success(request, f'Table {number} added successfully.')
            except Exception as e:
                messages.error(request, f'Error adding table: {str(e)}')
        
        elif action == 'delete':
            table_id = request.POST.get('table_id')
            try:
                table = Table.objects.get(id=table_id)
                table.delete()
                messages.success(request, f'Table {table.number} deleted successfully.')
            except Table.DoesNotExist:
                messages.error(request, 'Table not found.')
        
        return redirect('admin_tables')
    
    tables = Table.objects.all().order_by('number')
    occupied_tables = Table.objects.filter(
        reservations__date=datetime.now().date(),
        reservations__canceled=False
    )
    
    context = {
        'tables': tables,
        'occupied_tables': occupied_tables,
        'available_tables': tables.count() - occupied_tables.count()
    }
    return render(request, 'booking/admin/tables.html', context)

@user_passes_test(lambda u: u.is_staff)
def edit_table_view(request, pk):
    """Handle table editing."""
    table = get_object_or_404(Table, pk=pk)
    
    if request.method == 'POST':
        number = request.POST.get('number')
        capacity = request.POST.get('capacity')
        
        try:
            table.number = number
            table.capacity = capacity
            table.save()
            messages.success(request, f'Table {number} updated successfully.')
        except Exception as e:
            messages.error(request, f'Error updating table: {str(e)}')
        
        return redirect('admin_tables')
    
    return redirect('admin_tables')

@login_required
def check_availability_view(request):
    """Check table availability for a given date and time."""
    date_str = request.GET.get('date')
    time_str = request.GET.get('time')
    
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        time = datetime.strptime(time_str, '%H:%M').time()
        
        occupied_tables = Table.objects.filter(
            reservations__date=date,
            reservations__time__gte=(datetime.combine(date, time) - timedelta(hours=2)).time(),
            reservations__time__lt=(datetime.combine(date, time) + timedelta(hours=2)).time(),
            reservations__canceled=False
        ).values_list('id', flat=True)
        
        return JsonResponse({
            'occupied_tables': list(occupied_tables)
        })
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid date or time format'}, status=400)
