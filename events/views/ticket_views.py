from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from ..models import Ticket, PurchaseStatus
from ..utils import sync_ticket_payment


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
        try:
            if not sync_ticket_payment(ticket):
                ticket.delete()
        except Exception as e:
            # Log exception, but continue cleaning others
            print(f"Failed to delete expired ticket {ticket.ticket_code}: {e}")

    # Fetch all user's tickets efficiently
    tickets_qs = (
        Ticket.objects
        .filter(attendee=request.user)
        .select_related(
            "ticket_type",
            "ticket_type__event",
            "ticket_type__event__organizer"
        )
        .order_by(
            "ticket_type__event__start_time",
            "-purchase_date"
        )
    )

    # Group tickets by event ID for safety
    grouped_tickets = {}
    for ticket in tickets_qs:
        event_id = ticket.ticket_type.event.id
        if event_id not in grouped_tickets:
            grouped_tickets[event_id] = {
                "event": ticket.ticket_type.event,
                "tickets": []
            }
        grouped_tickets[event_id]["tickets"].append(ticket)

    return render(request, "events/ticket_templates/tickets.html", {
        "grouped_tickets": grouped_tickets,
        "tickets": tickets_qs,  # fallback if needed
    })


@login_required
def ticket_details(request, ticket_code):
    ticket = get_object_or_404(Ticket, ticket_code=ticket_code)

    # Security: ensure ticket belongs to the requesting user
    if ticket.attendee != request.user:
        messages.error(
            request, "You do not have permission to view this ticket.")
        return redirect("events:tickets")

    return render(request, 'events/ticket_templates/ticket_details.html', {
        "ticket": ticket
    })


@login_required
def download_ticket_pdf(request, ticket_code):
    messages.success(request, f"Ticket {ticket_code} Downloaded Successfully!")
    return redirect("events:ticket_details", ticket_code)
