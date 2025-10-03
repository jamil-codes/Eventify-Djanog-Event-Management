from urllib.parse import urljoin
from django.shortcuts import get_object_or_404, redirect, render
from ..models import Event, TicketType, Ticket, PurchaseStatus
from django.contrib.auth.decorators import login_required
from ..utils import get_stripe_checkout_url, sync_ticket_payment
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q
from decouple import config
import stripe

stripe.api_key = config("STRIPE_API_KEY")


@login_required
def buy_ticket(request, event_pk, ticket_type_pk):
    """
    Reserve a ticket (create pending ticket). Behavior:
    - Organizers get a free ticket immediately.
    - Enforce max_per_user for finalized tickets (PAID/FREE).
    - Do not count expired pending reservations as taken.
    - If user has an unexpired pending ticket, reuse it.
    - If user has an expired pending ticket, remove it and create a new one.
    """
    event = get_object_or_404(Event, pk=event_pk)
    ticket_type = get_object_or_404(TicketType, pk=ticket_type_pk, event=event)

    # Organizer bypasses limits (always gets a FREE ticket)
    if request.user == event.organizer:
        ticket = Ticket.objects.create(
            attendee=request.user,
            ticket_type=ticket_type,
            purchase_status=PurchaseStatus.FREE
        )
        messages.success(
            request, f"Free ticket claimed. Ticket ID: {ticket.ticket_code}")
        return redirect("events:event_detail", pk=event.pk)

    now = timezone.now()

    # Finalized   <<--is equals--->>   to paid/free
    finalized_count = Ticket.objects.filter(
        attendee=request.user,
        ticket_type=ticket_type,
        purchase_status__in=[PurchaseStatus.PAID, PurchaseStatus.FREE]
    ).count()

    if finalized_count >= ticket_type.max_per_user:
        messages.error(
            request, f"You cannot purchase more than {ticket_type.max_per_user} ticket(s) of this type.")
        return redirect("events:event_detail", pk=event.pk)

    # Check availability (PAID + PENDING unexpired)
    active_count = Ticket.objects.filter(
        ticket_type=ticket_type
    ).filter(
        Q(purchase_status=PurchaseStatus.PAID) |
        Q(purchase_status=PurchaseStatus.PENDING, reservation_expires_at__gt=now)
    ).count()

    if active_count >= ticket_type.quantity_available:
        messages.error(
            request, "Sorry — no tickets available of this type right now.")
        return redirect("events:event_detail", pk=event.pk)

    # Check for user's existing pending
    pending_ticket = Ticket.objects.filter(
        attendee=request.user,
        ticket_type=ticket_type,
        purchase_status=PurchaseStatus.PENDING
    ).first()

    if sync_ticket_payment(pending_ticket):
        messages.success(request, "Ticket already paid.")
        return redirect("events:event_detail", pk=event.pk)

    if pending_ticket:
        if pending_ticket.is_expired:
            pending_ticket.delete()
            ticket = Ticket.objects.create(
                attendee=request.user,
                ticket_type=ticket_type,
                purchase_status=PurchaseStatus.PENDING
            )
            messages.success(
                request, f"New reservation created. Ticket ID: {ticket.ticket_code}")
            return redirect("events:confirm_ticket_purchase",
                            event_pk=str(ticket.ticket_type.event.pk),
                            ticket_code=str(ticket.ticket_code))
        else:
            messages.info(
                request, f"You already have a pending ticket (ID: {pending_ticket.ticket_code}).")
            return redirect("events:confirm_ticket_purchase",
                            event_pk=str(pending_ticket.ticket_type.event.pk),
                            ticket_code=str(pending_ticket.ticket_code))

    # No pending -> create new
    ticket = Ticket.objects.create(
        attendee=request.user,
        ticket_type=ticket_type,
        purchase_status=PurchaseStatus.PENDING
    )
    messages.success(
        request, f"Ticket reserved. Ticket ID: {ticket.ticket_code}")
    return redirect("events:confirm_ticket_purchase",
                    event_pk=str(ticket.ticket_type.event.pk),
                    ticket_code=str(ticket.ticket_code))


# ========================= Confirm =========================
@login_required
def confirm_purchase(request, event_pk, ticket_code):
    """
    Show confirm page. Behavior:
    - If PAID: redirect with success message.
    - If expired: delete & redirect back to event.
    - Else: show confirm page with remaining time.
    - On POST: redirect to payments:start_checkout.
    """
    event = get_object_or_404(Event, pk=event_pk)
    ticket = get_object_or_404(
        Ticket, ticket_code=ticket_code, attendee=request.user)

    sync_ticket_payment(ticket)

    # Already paid → redirect
    if ticket.purchase_status == PurchaseStatus.PAID:
        messages.success(request, "This ticket is already paid and confirmed.")
        return redirect("events:event_detail", pk=event.pk)

    # Expired → delete & redirect
    if ticket.is_expired:
        ticket.delete()
        messages.error(
            request, "Your reservation expired. Please try booking again.")
        return redirect("events:event_detail", pk=event.pk)

    # Remaining time (seconds)
    remaining_seconds = None
    if ticket.reservation_expires_at:
        remaining_seconds = int(
            (ticket.reservation_expires_at - timezone.now()).total_seconds())

    # POST → payment
    if request.method == "POST":
        payments_url = reverse("payments:start_checkout",
                               args=[ticket.ticket_code])
        return redirect(payments_url)

    absolute_url = request.build_absolute_uri('/')  # ends with '/'
    success_path = reverse(
        "events:success_ticket_purchase",
        kwargs={'event_pk': str(event_pk), 'ticket_code': ticket_code}
    )
    cancel_path = reverse(
        "events:cancel_ticket_purchase",
        kwargs={'event_pk': event_pk, 'ticket_code': ticket_code}
    )

    success_url = urljoin(absolute_url, success_path)
    cancel_url = urljoin(absolute_url, cancel_path)
    checkout_url = get_stripe_checkout_url(ticket, success_url, cancel_url)

    return render(request, "events/ticket_templates/confirm_purchase.html", {
        "ticket": ticket,
        "event": event,
        "remaining_seconds": remaining_seconds,
        "checkout_url": checkout_url
    })


# ========================= Success =========================
@login_required
def success_ticket_purchase(request, event_pk, ticket_code):
    """
    Production-grade success view: verifies payment with Stripe
    before marking ticket as PAID. Overrides expiration if payment
    succeeded after reservation window expired.
    """
    ticket = get_object_or_404(
        Ticket, ticket_code=ticket_code, attendee=request.user)
    event = get_object_or_404(Event, pk=event_pk)

    if not ticket.stripe_session_id:
        messages.error(request, "❌ No Stripe session found for this ticket.")
        return redirect("events:event_detail", pk=event.pk)

    try:
        session = stripe.checkout.Session.retrieve(ticket.stripe_session_id)
    except stripe.error.StripeError:
        messages.error(
            request, "❌ Could not verify payment with Stripe. Try again later.")
        return redirect("events:event_detail", pk=event.pk)

    if session.payment_status == "paid":
        # Mark as PAID even if expired
        if ticket.purchase_status != PurchaseStatus.PAID:
            ticket.purchase_status = PurchaseStatus.PAID
            ticket.purchase_date = timezone.now()

            # Override reservation expiration if ticket was expired
            if ticket.is_expired:
                ticket.reservation_expires_at = timezone.now()  # optional, mark as finalized

            ticket.save(update_fields=[
                        'purchase_status', 'purchase_date', 'reservation_expires_at'])
            messages.success(
                request,
                f"✅ Payment successful! Ticket {ticket.ticket_code} is confirmed. "
                f"{'Note: Your reservation had expired, but payment is accepted.' if ticket.is_expired else ''}"
            )
        else:
            messages.info(
                request, f"Ticket {ticket.ticket_code} was already paid.")
    else:
        messages.warning(
            request, "⚠ Payment not completed. Ticket remains reserved or expired.")

    return redirect("events:event_detail", pk=event.pk)


# ========================= Cancelled =========================
@login_required
def cancel_ticket_purchase(request, event_pk, ticket_code):
    ticket = get_object_or_404(
        Ticket, ticket_code=ticket_code, attendee=request.user)

    if ticket.is_expired:
        messages.warning(
            request, f"⚠ Your reservation for ticket {ticket.ticket_code} expired.")
    else:
        messages.warning(
            request, f"⚠ Payment was canceled. Your ticket {ticket.ticket_code} is still reserved.")

    return redirect("events:confirm_ticket_purchase", event_pk=event_pk, ticket_code=ticket_code)
