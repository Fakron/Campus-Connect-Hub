from django.shortcuts import render
from .models import Event

def event(request):
    events = Event.objects.filter(display_on_home_page=True)
    return render(request, 'Event/event.html', {'current_event': events})
