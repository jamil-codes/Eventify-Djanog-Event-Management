from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from ..models import Ticket, PurchaseStatus


@login_required
def tickets(request):
    now = timezone.now()
    
    # Delete expired pending tickets (reservation timeout passed)
    expired_qs = Ticket.objects.filter(
        attendee=request.user,
        purchase_status=PurchaseStatus.PENDING,
        reservation_expires_at__lt=now
    )
    if expired_qs.exists():
        expired_qs.delete()

    # Fetch user's valid tickets, ordered logically
    tickets = (
        Ticket.objects
        .filter(attendee=request.user)
        .select_related(
            "ticket_type",
            "ticket_type__event",
            "ticket_type__event__organizer"
        )
        .order_by(
            "-purchase_date",     # newest first
            "ticket_type__event__start_time"
        )
    )

    return render(request, "events/ticket_templates/tickets.html", {
        "tickets": tickets,
    })
