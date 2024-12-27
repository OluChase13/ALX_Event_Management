from rest_framework import serializers
from .models import Event, Attendee
from django.utils.timezone import now


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['organizer', 'created_date', 'attendees_count']

    def validate_date_time(self, value):
        if value < now():
            raise serializers.ValidationError("Event date must be in the future.")
        return value


class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = ['event', 'user', 'registered_at']
        read_only_fields = ['registered_at']