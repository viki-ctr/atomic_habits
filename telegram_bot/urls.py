from django.urls import path

from telegram_bot import views

urlpatterns = [
    path('webhook/', views.telegram_webhook, name='telegram-webhook'),
    path('set-webhook/', views.set_webhook, name='set-webhook'),
]
