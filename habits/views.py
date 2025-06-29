from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.pagination import HabitPagination
from habits.permissions import IsOwner, IsPublicReadOnly
from habits.serializers import HabitSerializer, PublicHabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с привычками пользователя.
    Позволяет создавать, просматривать, обновлять и удалять привычки.
    """
    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        """Возвращает только привычки текущего пользователя"""
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Автоматически назначает текущего пользователя как владельца привычки"""
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        operation_description="Создание новой привычки",
        request_body=HabitSerializer,
        responses={
            status.HTTP_201_CREATED: HabitSerializer,
            status.HTTP_400_BAD_REQUEST: "Неверные данные",
            status.HTTP_401_UNAUTHORIZED: "Не авторизован"
        },
        security=[{'Bearer': []}]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class PublicHabitViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet только для чтения публичных привычек.
    Доступен всем пользователям без возможности редактирования.
    """
    serializer_class = PublicHabitSerializer
    pagination_class = HabitPagination
    permission_classes = [IsPublicReadOnly]

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)
