from rest_framework import serializers

from habits.models import Habit
from habits.validators import (validate_duration, validate_pleasant_habit, validate_related_habit,
                               validate_reward_or_related)


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('user', 'created_at')

    def validate(self, data):
        # Создаем временный объект привычки для валидации
        habit = Habit(**data)
        habit.user = self.context['request'].user

        validate_related_habit(habit)
        validate_reward_or_related(habit)
        validate_pleasant_habit(habit)

        if 'duration' in data:
            validate_duration(data['duration'])

        return data


class PublicHabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ('id', 'place', 'time', 'action', 'duration', 'is_public')
        read_only_fields = fields
