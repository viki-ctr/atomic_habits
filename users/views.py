from rest_framework import generics, permissions

from users.permissions import IsSelfOrReadOnly
from users.serializers import UserRegisterSerializer, UserSerializer


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


class UserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsSelfOrReadOnly]

    def get_object(self):
        return self.request.user
