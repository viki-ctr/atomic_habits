import logging
from datetime import datetime

import requests
from celery import shared_task
from django.conf import settings

from habits.models import Habit
from telegram_bot.models import TelegramUser

logger = logging.getLogger(__name__)


@shared_task
def send_telegram_reminders():
    """Отправка напоминаний с использованием модели TelegramUser"""
    now = datetime.now().time()
    habits = Habit.objects.filter(time__hour=now.hour, time__minute=now.minute)

    for habit in habits:
        try:
            telegram_user = TelegramUser.objects.filter(user=habit.user).first()
            if telegram_user:
                message = format_reminder_message(habit)
                send_telegram_message.delay(chat_id=telegram_user.chat_id, message=message)
        except Exception as e:
            logger.error(f"Ошибка отправки напоминания для пользователя {habit.user}: {e}")


@shared_task
def send_telegram_message(chat_id: int, message: str):
    """Отправка сообщения в Telegram"""
    try:
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"Ошибка отправки сообщения в Telegram: {e}")


def format_reminder_message(habit: Habit) -> str:
    """Форматирование сообщения-напоминания"""
    message = (
        f"⏰ *Напоминание о привычке*\n"
        f"*Действие:* {habit.action}\n"
        f"*Место:* {habit.place}\n"
        f"*Время на выполнение:* {habit.duration} сек.\n"
    )

    if habit.reward:
        message += f"\nПосле выполнения: *{habit.reward}* 🎁"
    elif habit.related_habit:
        message += f"\nПосле выполнения: *{habit.related_habit.action}* 😊"

    return message
