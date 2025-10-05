from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from ..models import Ticket, PurchaseStatus
from ..utils import sync_ticket_payment
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone
from weasyprint import HTML, CSS
import base64
import qrcode
import io


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

    qr_base64 = None
    if ticket.purchase_status in ['A', 'FRE']:
        qr_data = ticket.ticket_code
        qr_img = qrcode.make(qr_data)
        buffer = io.BytesIO()
        qr_img.save(buffer, format='PNG')
        qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    return render(request, 'events/ticket_templates/ticket_details.html', {
        "ticket": ticket,
        "qr_base64": qr_base64,
    })


@login_required
def download_ticket_pdf(request, ticket_code):
    ticket = get_object_or_404(Ticket, ticket_code=ticket_code)

    if ticket.attendee != request.user:
        messages.error(
            request, "You do not have permission to download this ticket.")
        return redirect("events:tickets")

    if ticket.purchase_status not in ['A', 'FRE']:
        messages.error(request, "This ticket is not available for download.")
        return redirect("events:tickets")

    # Generate QR as base64
    qr_img = qrcode.make(ticket.ticket_code)
    buffer = io.BytesIO()
    qr_img.save(buffer, format='PNG')
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    # Render HTML template
    html_string = render_to_string(
        "events/ticket_templates/pdf_template.html",
        {"ticket": ticket, "qr_base64": qr_base64, "request": request}
    )

    base_url = request.build_absolute_uri('/')

    # Add matching page CSS
    page_css = """
            @page {
            size: 680px 560px;
            margin: 0;
            }
            html, body {
            width: 680px;
            height: 555px;
            margin: 0;
            padding: 0;
            overflow: hidden;
            }
        """

    pdf = HTML(string=html_string, base_url=base_url).write_pdf(
        stylesheets=[CSS(string=page_css)]
    )

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=\"ticket_{ticket.ticket_code}.pdf\"'
    return response
