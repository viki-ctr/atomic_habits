import logging

from django.contrib.auth import authenticate
from asgiref.sync import sync_to_async
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters

from telegram_bot.models import TelegramUser

logger = logging.getLogger(__name__)

GET_CHAT_ID = 1


@sync_to_async
def authenticate_user(email, password):
    return authenticate(username=email, password=password)


@sync_to_async
def create_telegram_user(user, chat_id, username, first_name, last_name):
    TelegramUser.objects.update_or_create(
        user=user,
        defaults={
            'chat_id': chat_id,
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
        }
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(
        f"Привет, {user.first_name}!\n"
        "Я буду напоминать тебе о твоих привычках.\n"
        "Используй /connect чтобы привязать свой аккаунт."
    )


async def connect_account(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Пожалуйста, введите ваш email и пароль через пробел:\n"
        "Пример: user@example.com mypassword"
    )
    return GET_CHAT_ID


async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        email, password = update.message.text.split()
        user = await authenticate_user(email, password)

        if user:
            await create_telegram_user(
                user=user,
                chat_id=update.effective_chat.id,
                username=update.effective_user.username,
                first_name=update.effective_user.first_name,
                last_name=update.effective_user.last_name
            )
            await update.message.reply_text("✅ Аккаунт успешно привязан!")
            return ConversationHandler.END
        else:
            await update.message.reply_text("❌ Неверные учетные данные")
    except Exception as e:
        logger.error(f"Ошибка привязки аккаунта: {e}")
        await update.message.reply_text("⚠️ Ошибка. Проверьте формат ввода")
    return GET_CHAT_ID  # Остаемся в том же состоянии


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Действие отменено.")
    return ConversationHandler.END


def setup_handlers(application):
    """Настройка обработчиков команд"""
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('connect', connect_account)],
        states={
            GET_CHAT_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_chat_id)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(CommandHandler('start', start))
    application.add_handler(conv_handler)
