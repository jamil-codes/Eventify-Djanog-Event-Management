from django.shortcuts import render, redirect, get_object_or_404
from ..forms import EventForm
from ..models import Event, TicketType
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def events(request):
    events = Event.objects.all().order_by('-timestamp', '-pk')
    return render(request, 'events/event_templates/events.html', {'events': events})


@login_required
def add_event(request):
    if request.user.role != 'organizer':
        messages.error(
            request, 'Only organizers are allowed to create events!')
        return redirect('events:events')

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.orgenizer = request.user
            event.save()
            messages.success(request, 'Event created successfully!')
            return redirect('events:events')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EventForm()

    return render(request, 'events/event_templates/add_event.html', {'form': form})


def event_detail(requst, pk):
    event = get_object_or_404(Event, pk=pk)
    ticket_types = TicketType.objects.filter(event=event).order_by('price')
    return render(requst, 'events/event_templates/event_detail.html', {
        'event': event,
        'ticket_types': ticket_types
    })


@login_required
def edit_event(request, pk):
    event = get_object_or_404(Event, pk=pk, orgenizer=request.user)

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            event = form.save()
            messages.success(request, 'Event Saved successfully!')
            return redirect('events:event_detail', event.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EventForm(instance=event)

    return render(request, 'events/event_templates/edit_event.html', {
        'form': form,
        'event': event
    })
