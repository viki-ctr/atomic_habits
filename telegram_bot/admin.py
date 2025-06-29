from django.contrib import admin

from .models import TelegramUser


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'chat_id', 'username', 'created_at')
    search_fields = ('user__email', 'chat_id', 'username')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')
