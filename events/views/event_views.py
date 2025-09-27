from django.shortcuts import render, redirect, get_object_or_404
from ..forms import EventForm
from ..models import Event, TicketType
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from decouple import config
from django.utils import timezone

MAX_EVENTS_PER_PAGE = config('MAX_EVENTS_PER_PAGE', default=10)


def events(request):
    mine_param = request.GET.get("mine") == "1"

    # If "mine" and user is organizer/admin → show ALL their events (past + upcoming)
    if (
        mine_param
        and request.user.is_authenticated
        and request.user.role in ['organizer', 'admin']
    ):
        event_list = Event.objects.filter(
            organizer=request.user).order_by('-pk')
    else:
        # Base queryset: only organizers/admins, upcoming
        event_list = Event.objects.filter(
            organizer__role__in=['organizer', 'admin'],
            start_time__gte=timezone.now()
        ).order_by('start_time', 'pk')
        mine_param = False  # reset if not allowed

    # Pagination
    paginator = Paginator(event_list, MAX_EVENTS_PER_PAGE)
    page_number = request.GET.get('page')
    events = paginator.get_page(page_number)

    return render(request, 'events/event_templates/events.html', {
        'events': events,
        'mine': mine_param,
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
            return redirect('events:event_detail', event.pk)
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


@login_required
def delete_event(request, event_pk):
    event = get_object_or_404(Event, pk=event_pk, organizer=request.user)

    if request.method == "POST":
        event.delete()
        return redirect('events:events')

    return render(request, 'events/event_templates/delete_event.html', {
        'event': event,
    })
