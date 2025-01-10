from rest_framework import viewsets, pagination, filters, status
from .models import Event, Attendee, Comment
from .serializers import EventSerializer, AttendeeSerializer, CommentSerializer
from rest_framework import permissions
from rest_framework.response import Response
from datetime import datetime
from events.permissions import IsOrganizerOrReadOnly
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .filters import EventFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsOrganizerOrReadOnly]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['location', 'category', 'title']
    search_fields = ['title', 'location']
    ordering_fields = ['date_time', 'title']
    filterset_class = EventFilter       #Allows filtering options to be available on the API endpoint.
    pagination_class = pagination.PageNumberPagination



    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    def get_queryset(self):
        if self.action == 'list':
            return Event.objects.filter(date_time__gte=datetime.now())
        return super().get_queryset()


class AttendeeViewSet(viewsets.ModelViewSet):
    queryset = Attendee.objects.all()
    serializer_class = AttendeeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):                 #Adds user to waitlist if event is full
        event = serializer.validated_data['event']
        user = self.request.user
        
        if event.is_full():
            return Response({"error": "Event is full"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save(user=user, status='Registered')


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)