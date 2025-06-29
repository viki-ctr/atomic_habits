import json
import logging

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update
from telegram.ext import Application

logger = logging.getLogger(__name__)


application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()


def get_application():
    global _application
    if _application is None:
        _application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
    return _application


@csrf_exempt
def telegram_webhook(request):
    """Обработчик вебхука от Telegram"""
    if request.method == 'POST':
        try:
            application = get_application()
            data = json.loads(request.body.decode('utf-8'))
            update = Update.de_json(data, application.bot)
            application.process_update(update)
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            logger.error(f"Webhook error: {e}")
            return JsonResponse({'status': 'error'}, status=500)
    return JsonResponse({'status': 'method not allowed'}, status=405)


def set_webhook(request):
    """Установка вебхука (вызывается через админку или консоль)"""
    if request.method == 'GET':
        try:
            from django.urls import reverse
            webhook_url = f"https://{settings.DOMAIN}{reverse('telegram-webhook')}"
            result = application.bot.set_webhook(webhook_url)
            return JsonResponse({
                'status': 'success',
                'webhook_url': webhook_url,
                'result': result
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    return JsonResponse({'status': 'method not allowed'}, status=405)
