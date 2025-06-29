import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, patch

from django.test import TestCase, RequestFactory
from telegram.ext import ConversationHandler

from habits.models import Habit
from telegram_bot.handlers import cancel, get_chat_id, start, GET_CHAT_ID
from telegram_bot.models import TelegramUser
from telegram_bot.tasks import send_telegram_message, send_telegram_reminders
from telegram_bot.views import telegram_webhook
from users.models import User


class TelegramHandlersTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.update = AsyncMock()
        self.context = MagicMock()

        self.update.effective_user = MagicMock()
        self.update.effective_user.username = 'testuser'
        self.update.effective_user.first_name = 'Test'
        self.update.effective_user.last_name = 'User'
        self.update.effective_chat = MagicMock()
        self.update.effective_chat.id = '12345'
        self.update.message = AsyncMock()

    async def run_async(self, coro):
        """Запуск асинхронного кода в синхронных тестах"""
        return await coro

    @patch('telegram_bot.handlers.authenticate_user')
    @patch('telegram_bot.handlers.create_telegram_user')
    def test_get_chat_id_success(self, mock_create_telegram_user, mock_authenticate):
        """Тест успешной привязки аккаунта"""
        mock_authenticate.return_value = self.user
        self.update.message.text = 'test@example.com testpass123'

        result = asyncio.run(self.run_async(
            get_chat_id(self.update, self.context)
        ))

        self.assertEqual(result, ConversationHandler.END)
        mock_authenticate.assert_called_once_with('test@example.com', 'testpass123')
        mock_create_telegram_user.assert_called_once()
        self.update.message.reply_text.assert_awaited_once_with("✅ Аккаунт успешно привязан!")

    @patch('telegram_bot.handlers.authenticate_user')
    def test_get_chat_id_failure(self, mock_authenticate):
        """Тест неудачной привязки аккаунта"""
        mock_authenticate.return_value = None
        self.update.message.text = 'wrong@example.com wrongpass'

        result = asyncio.run(self.run_async(
            get_chat_id(self.update, self.context)
        ))

        self.assertEqual(result, GET_CHAT_ID)
        self.update.message.reply_text.assert_awaited_once_with("❌ Неверные учетные данные")

    def test_cancel_handler(self):
        """Тест обработчика отмены"""
        result = asyncio.run(self.run_async(
            cancel(self.update, self.context)
        ))

        self.assertEqual(result, ConversationHandler.END)
        self.update.message.reply_text.assert_awaited_once_with("Действие отменено.")

    def test_start_handler(self):
        """Тест стартового обработчика"""
        asyncio.run(self.run_async(
            start(self.update, self.context)
        ))

        self.update.message.reply_text.assert_awaited_once()


class TelegramTasksTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.telegram_user = TelegramUser.objects.create(
            user=self.user,
            chat_id='12345'
        )
        self.habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00:00",
            action="Пить воду",
            duration=60
        )

    @patch('telegram_bot.tasks.send_telegram_message.delay')
    def test_send_reminders(self, mock_send):
        from datetime import datetime
        now = datetime.now().time()
        self.habit.time = now
        self.habit.save()

        send_telegram_reminders()
        mock_send.assert_called_once()

    @patch('requests.post')
    def test_send_telegram_message(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        send_telegram_message('12345', 'Test message')
        mock_post.assert_called_once()


class TelegramWebhookTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.valid_data = {
            "update_id": 123,
            "message": {
                "message_id": 1,
                "date": 1630000000,
                "text": "Test",
                "chat": {"id": 1}
            }
        }
        self.invalid_data = "{bad: json}"

    def test_webhook_post_invalid_json(self):
        """Тест обработки невалидного JSON."""
        request = self.factory.post(
            '/webhook/',
            data=self.invalid_data,
            content_type='application/json'
        )
        response = telegram_webhook(request)
        self.assertEqual(response.status_code, 500)

    def test_webhook_wrong_method(self):
        """Тест на неподдерживаемый метод (GET)."""
        request = self.factory.get('/webhook/')
        response = telegram_webhook(request)
        self.assertEqual(response.status_code, 405)