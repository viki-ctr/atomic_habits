from django.conf import settings
from django.core.management.base import BaseCommand
from django.urls import reverse
from telegram import Bot


class Command(BaseCommand):
    help = 'Set Telegram webhook'

    def handle(self, *args, **options):
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        webhook_url = f"https://{settings.DOMAIN}{reverse('telegram-webhook')}"
        result = bot.set_webhook(webhook_url)
        self.stdout.write(
            self.style.SUCCESS(f'Webhook set to: {webhook_url}\nResult: {result}')
        )
