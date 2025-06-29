from django.core.exceptions import ValidationError


def validate_related_habit(habit):
    """Проверка что связанная привычка является приятной"""
    if habit.related_habit and not habit.related_habit.is_pleasant:
        raise ValidationError(
            "В связанные привычки могут попадать только привычки с признаком приятной привычки."
        )


def validate_reward_or_related(habit):
    """Проверка что указано либо вознаграждение, либо связанная привычка, но не оба"""
    if habit.reward and habit.related_habit:
        raise ValidationError(
            "Нельзя одновременно указывать связанную привычку и вознаграждение."
        )


def validate_pleasant_habit(habit):
    """Проверка что у приятной привычки нет вознаграждения или связанной привычки"""
    if habit.is_pleasant and (habit.reward or habit.related_habit):
        raise ValidationError(
            "У приятной привычки не может быть вознаграждения или связанной привычки."
        )


def validate_duration(value):
    """Проверка что время выполнения не больше 120 секунд"""
    if value > 120:
        raise ValidationError(
            "Время выполнения не должно превышать 120 секунд."
        )
