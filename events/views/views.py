from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from django.conf import settings
from django.db.models.functions import Trim
from events.models import Event, Contact


def index(request):
    # Latest or upcoming events
    events = (
        Event.objects.filter(start_time__gte=timezone.now())
        .order_by('start_time')[:6]
    )

    # Extract distinct popular locations (max 8)
    popular_locations = (
        Event.objects
        .filter(start_time__gte=timezone.now())
        .exclude(location__isnull=True)
        .exclude(location__exact='')
        .annotate(loc_trim=Trim('location'))
        .values_list('loc_trim', flat=True)
        .distinct()[:8]
    )

    context = {
        "events": events,
        "popular_locations": popular_locations,
    }

    return render(request, "index.html", context)


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        if not name or not email or not message:
            messages.error(request, "Please fill in all fields.")
            return redirect("index")

        try:
            Contact.objects.create(name=name, email=email, message=message)
            messages.success(
                request, "Your message has been sent successfully!")
        except Exception as e:
            messages.error(request, f"Error sending email: {e}")

        return redirect("index")

    return redirect("index")
