from django.db import models
from django.conf import settings
from django.utils.timezone import now
from users.models import CustomUser  

CATEGORY_CHOICES = [
    ('Conference', 'Conference'),
    ('Workshop', 'Workshop'),
    ('Concert', 'Concert'),
    ('Wedding', 'Wedding'),
    ('Seminar', 'Seminar'),
]

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='events')
    capacity = models.PositiveIntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    attendees_count = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='conference')



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
        unique_together = ('event', 'user')             # Prevent duplicate registrations

    def __str__(self):
        return f"{self.user.username} attending {self.event.title}"
    

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="comments")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Comment by {self.user.username} on {self.event.title}"
