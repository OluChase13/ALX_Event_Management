from rest_framework.permissions import BasePermission

class IsOrganizerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.organizer == request.user