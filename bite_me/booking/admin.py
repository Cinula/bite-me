# booking/admin.py

from django.contrib import admin
from .models import Table, Reservation, Contact, EmailLog

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'capacity')


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'time', 'guests', 'canceled')
    list_filter = ('date', 'canceled')
    search_fields = ('user__username',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected messages as unread"

    actions = ['mark_as_read', 'mark_as_unread']


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ('email_to', 'email_type', 'subject', 'status', 'created_at', 'sent_at')
    list_filter = ('email_type', 'status', 'created_at')
    search_fields = ('email_to', 'subject', 'message', 'error_message')
    readonly_fields = ('created_at', 'sent_at')
    ordering = ('-created_at',)
    
    def has_add_permission(self, request):
        return False  # Prevent manual creation of logs
