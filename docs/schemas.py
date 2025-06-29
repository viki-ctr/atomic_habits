from drf_yasg import openapi

habit_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'place': openapi.Schema(type=openapi.TYPE_STRING, description='Место выполнения'),
        'time': openapi.Schema(type=openapi.TYPE_STRING, format='time', description='Время выполнения'),
        'action': openapi.Schema(type=openapi.TYPE_STRING, description='Действие'),
        'is_pleasant': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Признак приятной привычки'),
        'related_habit': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID связанной привычки'),
        'frequency': openapi.Schema(type=openapi.TYPE_INTEGER, description='Периодичность (1-7 дней)'),
        'reward': openapi.Schema(type=openapi.TYPE_STRING, description='Вознаграждение'),
        'duration': openapi.Schema(type=openapi.TYPE_INTEGER, description='Длительность (секунды)'),
        'is_public': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Публичная привычка'),
    },
    required=['place', 'time', 'action', 'duration']
)
