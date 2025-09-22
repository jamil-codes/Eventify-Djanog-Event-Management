from django.shortcuts import render, redirect
from .forms import EventForm
from .models import Event
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def events(request):
    return render(request, 'events/events.html')


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

    return render(request, 'events/add_event.html', {'form': form})
