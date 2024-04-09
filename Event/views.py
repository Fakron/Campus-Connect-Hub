from django.shortcuts import render
from .models import Event

def event(request):
    events = Event.objects.filter(display_on_home_page=True)

    if events:
        return render(request, 'Event/eventdetails.html', {'current_events': events})
    else:
        return render(request, "Event,commingevent.html")

