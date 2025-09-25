from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Event, TicketType
from ..forms import TicketTypeForm


@login_required
def add_ticket_type(request, event_pk):
    event = get_object_or_404(Event, pk=event_pk, organizer=request.user)
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


@login_required
def edit_ticket_type(request, event_pk, ticket_type_pk):
    event = get_object_or_404(Event, pk=event_pk, organizer=request.user)
    ticket_type = get_object_or_404(
        TicketType, pk=ticket_type_pk, event=event)
    if request.method == "POST":
        form = TicketTypeForm(request.POST, instance=ticket_type)
        if form.is_valid():
            form.save()
            return redirect('events:event_detail', event.pk)

    else:
        form = TicketTypeForm(instance=ticket_type)
    return render(request, 'events/ticket_templates/edit_ticket_type.html', {
        'form': form,
        'event': event,
        'ticket_type': ticket_type
    })


@login_required
def delete_ticket_type(request, event_pk, ticket_type_pk):
    event = get_object_or_404(Event, pk=event_pk, organizer=request.user)
    ticket_type = get_object_or_404(TicketType, pk=ticket_type_pk, event=event)

    if request.method == "POST":
        ticket_type.delete()
        return redirect('events:event_detail', event.pk)

    return render(request, 'events/ticket_templates/delete_ticket_type.html', {
        'event': event,
        'ticket_type': ticket_type,
    })
