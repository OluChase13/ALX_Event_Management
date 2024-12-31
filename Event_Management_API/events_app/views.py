from rest_framework import generics, permissions, filters, status, pagination
from rest_framework.response import Response
from django.utils.timezone import now
from django.utils import timezone
from .models import Event, Attendee, Comment
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .serializers import EventSerializer, AttendeeSerializer, CommentSerializer
from .permissions import IsOrganizer
from rest_framework.exceptions import ValidationError


class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.filter(date_time__gte=now()).order_by('date_time')
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['location']
    search_fields = ['title', 'location']
    ordering_fields = ['date_time', 'title']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = pagination.PageNumberPagination


    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrganizer]

    def get_queryset(self):
        return self.queryset.filter(organizer=self.request.user)
    

class AttendeeCreateView(generics.CreateAPIView):
    queryset = Attendee.objects.all()
    serializer_class = AttendeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        event_id = request.data.get('event')
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return Response({"detail": "Event not found."}, status=status.HTTP_404_NOT_FOUND)

        if Attendee.objects.filter(user=request.user, event=event).exists():
            return Response({"detail": "You are already registered for this event."}, status=status.HTTP_400_BAD_REQUEST)
        if event.attendees.count() >= event.capacity:
            return Response({"detail": "Event is at full capacity."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, event=event)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AttendeeListView(generics.ListAPIView):
    serializer_class = AttendeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        event_id = self.kwargs['event_id']
        return Attendee.objects.filter(event_id=event_id)
    

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        event_id = self.kwargs['event_pk']
        return Comment.objects.filter(event_id=event_id).order_by('-created_at')

    def perform_create(self, serializer):
        event = Event.objects.get(pk=self.kwargs['event_pk'])
        serializer.save(user=self.request.user, event=event)

class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        event_id = self.kwargs['event_pk']
        return Comment.objects.filter(event_id=event_id)

    def perform_update(self, serializer):
        comment = self.get_object()
        if comment.user != self.request.user:
            raise ValidationError("You do not have permission to update this comment.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise ValidationError("You do not have permission to delete this comment.")
        instance.delete()
