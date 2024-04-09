from django.db import models

class Speaker(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    image = models.ImageField(upload_to='speakers/', blank=True, null=True)
    
    def __str__(self):
        return self.name

class Sponsor(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='sponsors/', blank=True, null=True)
    
    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=100)
    sub_title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()
    location = models.CharField(max_length=100)
    date = models.DateTimeField()
    promo_video = models.URLField(blank=True, null=True)
    event_image = models.ImageField(upload_to='event_front/', blank=True, null=True)
    cover_image = models.ImageField(upload_to='event_covers/', blank=True, null=True)
    display_on_home_page = models.BooleanField(default=False)
    speakers = models.ManyToManyField(Speaker, related_name='events', blank=True)
    sponsors = models.ManyToManyField(Sponsor, related_name='events', blank=True)

    def __str__(self):
        return f'Event Name - {self.title} Status - {self.display_on_home_page}'
