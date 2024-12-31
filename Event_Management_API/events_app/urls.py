from django.urls import path
from .views import EventListCreateView, EventDetailView, AttendeeCreateView, AttendeeListView, CommentListCreateView, CommentRetrieveUpdateDestroyView


urlpatterns = [
    path('', EventListCreateView.as_view(), name='event-list'),
    path('<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('events_app/<int:event_id>/register/', AttendeeCreateView.as_view(), name='event-register'),
    path('events_app/<int:event_id>/attendees/', AttendeeListView.as_view(), name='event-attendees'),
    path('events_app/<int:event_pk>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('events_app/<int:event_pk>/comments/<int:pk>/', CommentRetrieveUpdateDestroyView.as_view(), name='comment-retrieve-update-destroy'),
]
