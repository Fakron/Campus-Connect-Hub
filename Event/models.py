from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    display_on_home_page = models.BooleanField(default=False)
    promo_video = models.URLField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='event_covers/', blank=True, null=True)  

    
    def __str__(self):
        return f'Event Name -{self.name}   Status-{self.display_on_home_page}'
    