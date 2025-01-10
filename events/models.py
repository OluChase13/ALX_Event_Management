from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from users.models import CustomUser
from django.conf import settings
from django.utils import timezone


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
    date_time = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=255)
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="organized_events")
    capacity = models.PositiveIntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='conference')
    is_recurring = models.BooleanField(default=False)
    recurrence_interval = models.CharField(max_length=50, null=True, blank=True, choices=[
        ('Daily', 'Daily'),
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
    ])
    
    def is_upcoming(self):
        return self.date_time > now()

    def is_full(self):
        return self.attendees.count() >= self.capacity



class Attendee(models.Model):

    STATUS_CHOICES = [
        ('registered', 'registered'),
        ('waitlisted', 'Waitlisted'),
        ('cancelled', 'Cancelled'),
    ]

    event = models.ForeignKey(Event, related_name='attendees', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='attendances', on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='confirmed')   #Tracks whether the user is registered or on the waitlist.

    class Meta:
        unique_together = ('event', 'user')    #Ensures that a user cannot register for the same event more than once.

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"



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