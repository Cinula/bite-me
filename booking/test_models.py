from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, time
from .models import Table, Reservation, Contact, EmailLog

class BookingModelTests(TestCase):
    """Unit tests for the models in the booking app."""

    def setUp(self):
        """Set up test user, table, reservation, contact, and email log."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.table = Table.objects.create(number="A1", capacity=4)

        self.reservation = Reservation.objects.create(
            user=self.user,
            date=date(2025, 4, 15),
            time=time(18, 30),
            guests=2
        )
        self.reservation.tables.add(self.table)

        self.contact = Contact.objects.create(
            name="Alice",
            email="alice@example.com",
            subject="Booking Question",
            message="Can I book a table for 5?"
        )

        self.email_log = EmailLog.objects.create(
            email_to="bob@example.com",
            email_type="welcome",
            subject="Welcome to Bite Me",
            message="Thanks for signing up!",
            status="success"
        )

    def test_table_str(self):
        """Table __str__ should return its number and capacity."""
        self.assertEqual(str(self.table), "Table A1 (Capacity: 4)")

    def test_reservation_str(self):
        """Reservation __str__ should return formatted info about the booking."""
        expected = f"Reservation by {self.user.username} on {self.reservation.date} at {self.reservation.time} for 2 guests"
        self.assertEqual(str(self.reservation), expected)

    def test_reservation_table_relationship(self):
        """Reservation should be linked to the correct table(s)."""
        self.assertIn(self.table, self.reservation.tables.all())

    def test_contact_str(self):
        """Contact __str__ should return subject and name."""
        self.assertEqual(str(self.contact), "Booking Question - Alice")

    def test_email_log_str(self):
        """EmailLog __str__ should show email type, recipient, and status."""
        self.assertEqual(str(self.email_log), "welcome to bob@example.com - success")

    def test_email_log_defaults(self):
        """EmailLog should have default status and no sent_at initially."""
        self.assertEqual(self.email_log.status, "success")
        self.assertIsNone(self.email_log.sent_at)