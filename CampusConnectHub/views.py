from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from Event.models import Event

def home(request):
    current_time = timezone.now()
    current_event = Event.objects.filter(display_on_home_page=True, date__gt=current_time).order_by('date').first()
    time_remaining = None
    if current_event:
        time_remaining = current_event.date - current_time
    
    return render(request, 'Account/home.html', {'current_event': current_event, 'time_remaining': time_remaining})
