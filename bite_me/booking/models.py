# booking/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Table(models.Model):
    number = models.CharField(max_length=10)
    capacity = models.IntegerField()

    class Meta:
        ordering = ['number']

    def __str__(self):
        return f"Table {self.number} (Capacity: {self.capacity})"


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    date = models.DateField()
    time = models.TimeField()
    guests = models.IntegerField()
    tables = models.ManyToManyField(Table, related_name='reservations', blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    canceled = models.BooleanField(default=False)

    def __str__(self):
        return f"Reservation by {self.user.username} on {self.date} at {self.time} for {self.guests} guests"


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject} - {self.name}"
