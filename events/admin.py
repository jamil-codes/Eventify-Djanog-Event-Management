from django.contrib import admin
from .models import Ticket, TicketType, Event


admin.site.register(Event)


admin.site.register(Ticket)
admin.site.register(TicketType)
