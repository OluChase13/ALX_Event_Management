from rest_framework import generics
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class UserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
