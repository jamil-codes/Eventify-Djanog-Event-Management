from django.db import models
from django.conf import settings
from datetime import datetime

User = settings.AUTH_USER_MODEL


class Event(models.Model):
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
    Paid = "0", "Paid"
    Cancelled = "1", "Cancelled"
    Checked_in = "2", "Checked_in"


class Ticket(models.Model):
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='tickets'
    )
    attendee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tickets'
    )
    status = models.CharField(
        max_length=1, choices=TicketStatus.choices, default=TicketStatus.Checked_in
    )

    def __str__(self):
        return f'{self.ticket_type.name} Ticket for -> {self.event.title} by {self.event.orgernizer}'
