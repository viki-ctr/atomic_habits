import logging

from django.apps import AppConfig
from django.conf import settings

logger = logging.getLogger(__name__)


class TelegramBotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'telegram_bot'
    _is_initialized = False

    def ready(self):
        """Инициализация бота при запуске приложения"""
        if not self._is_initialized and not settings.DEBUG:
            try:
                from telegram.ext import Application

                from .handlers import setup_handlers

                self._is_initialized = True
                application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
                setup_handlers(application)

                logger.info("Starting Telegram bot in polling mode...")
                application.run_polling()
            except Exception as e:
                logger.error(f"Error initializing Telegram bot: {e}")
                self._is_initialized = False

    async def initialize_bot(self):
        """Асинхронная инициализация бота"""
        from telegram.ext import Application

        from .handlers import setup_handlers

        application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
        setup_handlers(application)

        if settings.DEBUG:
            await application.initialize()
            await application.start()
            await application.updater.start_polling()
