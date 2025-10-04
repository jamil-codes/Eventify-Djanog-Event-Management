from django.contrib.auth.decorators import login_required
from ..models import Ticket, PurchaseStatus
from ..utils import sync_ticket_payment
from django.shortcuts import render
from django.utils import timezone
from django.contrib import messages


@login_required
def tickets(request):
    now = timezone.now()

    # Clean up expired reservations
    expired_qs = Ticket.objects.filter(
        attendee=request.user,
        purchase_status=PurchaseStatus.PENDING,
        reservation_expires_at__lt=now
    )

    for ticket in expired_qs:
        if not sync_ticket_payment(ticket):
            ticket.delete()

    # Fetch all user's tickets efficiently
    tickets = (
        Ticket.objects
        .filter(attendee=request.user)
        .select_related(
            "ticket_type",
            "ticket_type__event",
            "ticket_type__event__organizer"
        )
        .order_by(
            # Group by event time (soonest first)
            "ticket_type__event__start_time",
            "-purchase_date"                   # Within event, newest ticket first
        )
    )

    # Optional grouping by event for the template (cleaner UX)
    grouped_tickets = {}
    for ticket in tickets:
        event = ticket.ticket_type.event
        if event not in grouped_tickets:
            grouped_tickets[event] = []
        grouped_tickets[event].append(ticket)

    return render(request, "events/ticket_templates/tickets.html", {
        "grouped_tickets": grouped_tickets,
        "tickets": tickets,  # kept for fallback
    })
