from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from booking.models import Table, Reservation
from datetime import datetime, timedelta

# Create your tests here.

class BookingViewTests(TestCase):
    """Tests for key views in the booking app that require user authentication."""

    def setUp(self):
        """Create a test user and a table for reservation tests."""
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.table = Table.objects.create(number='A1', capacity=4)

    def test_create_reservation_redirects_if_not_logged_in(self):
        """Anonymous users should be redirected to the login page when accessing the booking form."""
        response = self.client.get(reverse('book'))  # Adjust to your URL name
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)

    def test_create_reservation_view_logged_in(self):
        """Logged-in users should access the reservation form successfully."""
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('book'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/booking_form.html')

    def test_my_bookings_requires_login(self):
        """Accessing the bookings list without being logged in should redirect to login."""
        response = self.client.get(reverse('my_bookings'))  # Adjust if needed
        self.assertEqual(response.status_code, 302)

    def test_my_bookings_view_logged_in(self):
        """Logged-in users should see their bookings using the correct template."""
        Reservation.objects.create(
            user=self.user,
            date=datetime.now().date() + timedelta(days=1),
            time=datetime.now().time(),
            guests=2
        )
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('my_bookings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/bookings_list.html')