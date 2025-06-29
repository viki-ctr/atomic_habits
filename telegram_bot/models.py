from django.db import models

from users.models import User


class TelegramUser(models.Model):
    """Модель для хранения данных пользователей Telegram"""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='telegram_user'
    )
    chat_id = models.CharField(max_length=50, unique=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} ({self.chat_id})"

    class Meta:
        verbose_name = 'Telegram пользователь'
        verbose_name_plural = 'Telegram пользователи'
