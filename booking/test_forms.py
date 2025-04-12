from django.test import TestCase
from booking.forms import ReservationForm
from datetime import datetime, timedelta

# Create your tests here.


class ReservationFormTests(TestCase):
    def setUp(self):
        self.today = datetime.now().date()
        self.valid_data = {
            'date': self.today + timedelta(days=1),
            'time': '12:00',
            'guests': 4
        }

    def test_valid_reservation_form(self):
        """Form should be valid with correct data."""
        form = ReservationForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_past_date_rejected(self):
        """Form should reject past dates."""
        data = self.valid_data.copy()
        data['date'] = self.today - timedelta(days=1)
        form = ReservationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors)

    def test_over_30_days_rejected(self):
        """Form should reject dates more than 30 days out."""
        data = self.valid_data.copy()
        data['date'] = self.today + timedelta(days=31)
        form = ReservationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors)

    def test_invalid_time_rejected(self):
        """Form should reject times outside 11:00–22:00."""
        data = self.valid_data.copy()
        data['time'] = '09:00'
        form = ReservationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('time', form.errors)

    def test_invalid_guest_count(self):
        """Form should reject guest count < 1 or > 20."""
        for invalid_guests in [0, 21]:
            data = self.valid_data.copy()
            data['guests'] = invalid_guests
            form = ReservationForm(data=data)
            self.assertFalse(form.is_valid())
            self.assertIn('guests', form.errors)