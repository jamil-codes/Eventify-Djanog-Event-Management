# events/admin.py
from django.contrib import admin
from .models import Ticket, TicketType, Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["title", "organizer", "start_time", "location"]
    search_fields = ["title", "organizer__username", "location"]
    list_filter = ["start_time"]
    ordering = ["-start_time"]


@admin.register(TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "event", "price",
                    "quantity_available", "max_per_user"]
    search_fields = ["name", "event__title"]
    list_filter = ["event"]
    ordering = ["event", "name"]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = [
        "ticket_code",
        "attendee",
        "ticket_type",
        "event_title",
        "purchase_status",
        "status",
        "purchase_date",
        "reservation_expires_at",
        "is_expired_display",
    ]
    list_filter = ["purchase_status", "status", "ticket_type__event"]
    search_fields = ["ticket_code", "attendee__username",
                     "ticket_type__name", "ticket_type__event__title"]
    readonly_fields = ["ticket_code", "purchase_date",
                       "stripe_price", "is_expired", "reservation_seconds_left", "stripe_product_id", "stripe_price_id", "stripe_session_id"]

    def event_title(self, obj):
        return obj.ticket_type.event.title
    event_title.short_description = "Event"

    def is_expired_display(self, obj):
        return "✅ Yes" if obj.is_expired else "❌ No"
    is_expired_display.short_description = "Expired?"
