from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from django.utils.timezone import now
from .models import Event, Attendee
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import EventSerializer, AttendeeSerializer
from .permissions import IsOrganizer


class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.filter(date_time__gte=now()).order_by('date_time')
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['location']
    search_fields = ['title', 'location']
    ordering_fields = ['date_time', 'title']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrganizer]

    def get_queryset(self):
        return self.queryset.filter(organizer=self.request.user)
    

class RegisterForEventView(generics.CreateAPIView):
    serializer_class = AttendeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        event = Event.objects.get(pk=self.kwargs['pk'])
        if event.is_full():
            return Response({"error": "Event is full."}, status=status.HTTP_400_BAD_REQUEST)
        attendee, created = Attendee.objects.get_or_create(event=event, user=request.user)
        if not created:
            return Response({"error": "You are already registered."}, status=status.HTTP_400_BAD_REQUEST)
        event.attendees_count += 1
        event.save()
        return Response({"message": "Registered successfully!"}, status=status.HTTP_201_CREATED)

