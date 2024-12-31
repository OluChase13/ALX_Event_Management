from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.utils.timezone import now
from .models import Event, Notification
from datetime import timedelta

@receiver(post_save, sender=Event)
def send_event_notification(sender, instance, created, **kwargs):
    if created:
        return
    if instance.date_time - now() <= timedelta(days=3):  # Send 3 days before event
        users = instance.attendees.all()
        for user in users:
            notification = Notification.objects.create(
                user=user,
                event=instance,
                message=f"Reminder: The event '{instance.title}' is coming up in 3 days!"
            )
            send_mail(
                'Event Reminder',
                notification.message,
                'from@example.com',
                [user.email],
                fail_silently=False,
            )