from django.db import models
from django.conf import settings
from django.utils.timezone import now

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='events')
    capacity = models.PositiveIntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    attendees_count = models.PositiveIntegerField(default=0)


    def is_upcoming(self):
        return self.date_time > now()
    
    def register_attendee(self):
        """ Registers an attendee and updates the capacity """
        if self.attendee_count < self.capacity:
            self.attendee_count += 1
            self.save()
            return True
        return False  # Return False if capacity is full
    
    def __str__(self):
        return self.title

class Attendee(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="attendees")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'user')

    def __str__(self):
        return f"{self.user.username} -> {self.event.title}"
