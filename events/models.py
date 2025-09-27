import uuid
from django.db import models
from django.conf import settings
from datetime import datetime
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
    start_time = models.DateTimeField(default=datetime.now)
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


class Ticket(models.Model):
    id = models.BigAutoField(primary_key=True)
    ticket_code = models.CharField(
        max_length=50,
        unique=True,
        editable=False
    )
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='tickets'
    )
    attendee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tickets'
    )

    class TicketStatus(models.TextChoices):
        NOT_CHECKED_IN = "N", _("Not Checked-In")
        CHECKED_IN = "C", _("Checked-In")
        CANCELLED = "X", _("Cancelled")

    status = models.CharField(
        max_length=1,
        choices=TicketStatus.choices,
        default=TicketStatus.NOT_CHECKED_IN
    )

    def save(self, *args, **kwargs):
        if not self.ticket_code:
            self.ticket_code = f"TCK-{self.purchase_date.strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.ticket_code} | {self.ticket_type.name} for {self.event.title}'
