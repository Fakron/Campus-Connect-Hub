from django.shortcuts import render
from django.utils import timezone
from Event.models import Event
import json

def home(request):
    current_time = timezone.now()
    current_event = Event.objects.filter(display_on_home_page=True, date__gt=current_time).order_by('date').first()
    time_remaining = None
    user = request.user
    time_remaining_js = None
    if current_event:
        time_remaining = current_event.date - current_time
        time_remaining_seconds = time_remaining.total_seconds()
        days = int(time_remaining_seconds // (24 * 3600))
        time_remaining_seconds = time_remaining_seconds % (24 * 3600)
        hours = int(time_remaining_seconds // 3600)
        time_remaining_seconds %= 3600
        minutes = int(time_remaining_seconds // 60)
        seconds = int(time_remaining_seconds % 60)
        time_remaining_js = f"var countDownDate = new Date('{current_event.date.strftime('%b %d, %Y')} {current_event.date.strftime('%H:%M:%S')}').getTime();"
        print(time_remaining_js)
    
    return render(request, 'Account/home.html', {'current_event': current_event, 'time_remaining': time_remaining, 'time_remaining_js': time_remaining_js, 'user':user})
