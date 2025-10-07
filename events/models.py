from datetime import timedelta
import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

User = settings.AUTH_USER_MODEL


class Event(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField(default=timezone.now)
    location = models.TextField()
    image = models.ImageField(upload_to='events/')
    organizer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="events"
    )

    def __str__(self):
        return f'{self.title} by {self.organizer}'


class TicketType(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='ticket_types'
    )
    name = models.CharField(max_length=100)  # removed global unique=True
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.PositiveIntegerField()
    max_per_user = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('event', 'name')  # enforce per-event uniqueness
        verbose_name = "Ticket Type"
        verbose_name_plural = "Ticket Types"

    def __str__(self):
        return f"{self.name} for {self.event.title}"


class TicketStatus(models.TextChoices):
    NOT_CHECKED_IN = "N", _("Not Checked-In")
    CHECKED_IN = "C", _("Checked-In")
    CANCELLED = "X", _("Cancelled")


class PurchaseStatus(models.TextChoices):
    PENDING = "P", _("Pending")
    PAID = "A", _("Paid")
    REFUNDED = "R", _("Refunded")
    FAILED = "F", _("Failed")
    FREE = "FRE", _("Free")  # for organizers or comped tickets


class Ticket(models.Model):
    id = models.BigAutoField(primary_key=True)
    ticket_code = models.CharField(max_length=50, unique=True, editable=False)
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE)
    stripe_product_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_price_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_price = models.PositiveBigIntegerField(default=0)
    purchase_date = models.DateTimeField(
        default=timezone.now)  # timezone-aware
    attendee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tickets')

    purchase_status = models.CharField(
        max_length=3,
        choices=PurchaseStatus.choices,
        default=PurchaseStatus.PENDING
    )

    status = models.CharField(
        max_length=1,
        choices=TicketStatus.choices,
        default=TicketStatus.NOT_CHECKED_IN
    )

    # reservation_expires_at keeps the reservation window (nullable)
    reservation_expires_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # ensure purchase_date is timezone-aware
        if not self.purchase_date:
            self.purchase_date = timezone.now()

        # Auto calculate stripe price (cents)
        try:
            self.stripe_price = int(self.ticket_type.price * 100)
        except Exception:
            self.stripe_price = 0

        # Generate ticket code if missing
        if not self.ticket_code:
            ts = self.purchase_date.strftime('%Y%m%d%H%M%S')
            self.ticket_code = f"TCK-{ts}-{uuid.uuid4().hex[:6].upper()}"

        # If pending and no expiry set, set default 15 minutes from now
        if self.purchase_status == PurchaseStatus.PENDING and not self.reservation_expires_at:
            self.reservation_expires_at = timezone.now() + timedelta(minutes=15)

        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        """True when ticket was pending and reservation_expires_at passed."""
        return (
            self.purchase_status == PurchaseStatus.PENDING
            and self.reservation_expires_at is not None
            and timezone.now() > self.reservation_expires_at
        )

    @property
    def reservation_seconds_left(self):
        """Returns seconds remaining (int) or 0 if expired/not set."""
        if not self.reservation_expires_at:
            return 0
        delta = self.reservation_expires_at - timezone.now()
        return max(int(delta.total_seconds()), 0)

    def __str__(self):
        return f'{self.ticket_code} | {self.ticket_type.name} for {self.ticket_type.event.title}'


class Contact(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField(max_length=254)
    message = models.TextField(blank=False)

    def __str__(self):
        return f'{self.name} + ({self.email})'
