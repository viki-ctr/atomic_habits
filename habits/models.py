from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    place = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.CharField(max_length=255)
    is_pleasant = models.BooleanField(default=False)
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    frequency = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(7)]
    )
    reward = models.CharField(max_length=255, blank=True)
    duration = models.PositiveIntegerField(validators=[MaxValueValidator(120)])
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.related_habit and self.reward:
            raise ValidationError("Нельзя одновременно указывать связанную привычку и вознаграждение.")
        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError("Связанная привычка должна быть приятной.")
        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError("Приятная привычка не может иметь вознаграждения или связанной привычки.")

    def __str__(self):
        return f"{self.action} в {self.time} ({self.user})"

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['-created_at']
