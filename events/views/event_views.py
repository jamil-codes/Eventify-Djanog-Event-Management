from django.shortcuts import render, redirect, get_object_or_404
from ..forms import EventForm
from ..models import Event, TicketType
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from decouple import config

MAX_EVENTS_PER_PAGE = config('MAX_EVENTS_PER_PAGE', default=10)


def events(request):
    # Show only events created by organizers or admins
    event_list = Event.objects.filter(
        organizer__role__in=['organizer', 'admin']
    ).order_by('-start_time', '-pk')

    # Pagination (10 events per page, adjust as needed)
    paginator = Paginator(event_list, MAX_EVENTS_PER_PAGE)
    page_number = request.GET.get('page')
    events = paginator.get_page(page_number)

    return render(request, 'events/event_templates/events.html', {
        'events': events
    })


@login_required
def add_event(request):
    if request.user.role not in ['organizer', 'admin']:
        messages.error(request, 'Only organizers or admins can create events!')
        return redirect('events:events')

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            messages.success(request, 'Event created successfully!')
            return redirect('events:events')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EventForm()

    return render(request, 'events/event_templates/add_event.html', {'form': form})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    can_add_ticket = (
        request.user.is_authenticated
        and request.user.role in ['organizer', 'admin']
        and request.user == event.organizer
    )

    ticket_types = TicketType.objects.filter(event=event).order_by('price')
    return render(request, 'events/event_templates/event_detail.html', {
        'event': event,
        'ticket_types': ticket_types,
        'can_add_ticket': can_add_ticket
    })


@login_required
def edit_event(request, pk):
    event = get_object_or_404(Event, pk=pk, organizer=request.user)

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('events:event_detail', pk=event.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EventForm(instance=event)

    return render(request, 'events/event_templates/edit_event.html', {
        'form': form,
        'event': event
    })
