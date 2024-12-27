from django.urls import path
from .views import EventListCreateView, EventDetailView, RegisterForEventView

urlpatterns = [
    path('', EventListCreateView.as_view(), name='event-list'),
    path('<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('events_app/<int:pk>/register/', RegisterForEventView.as_view(), name='register-for-event'),

]
