from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Event
from ..forms import TicketTypeForm


@login_required
def add_ticket_type(request, pk):
    event = get_object_or_404(Event, pk=pk, orgenizer=request.user)
    if request.method == "POST":
        form = TicketTypeForm(request.POST)
        if form.is_valid():
            ticket_type = form.save(commit=False)
            ticket_type.event = event
            ticket_type.save() 
            return redirect('events:event_detail', event.pk)

    else:
        form = TicketTypeForm()
    return render(request, 'events/ticket_templates/add_ticket_type.html', {
        'form': form,
        'event': event
    })
