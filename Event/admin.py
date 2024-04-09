from django.contrib import admin

from .models import Event,Sponsor,Speaker
# Register your models here.

admin.site.register(Event)
admin.site.register(Speaker)
admin.site.register(Sponsor)