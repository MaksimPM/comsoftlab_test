from django.urls import path
from mail.apps import MailConfig
from mail.views import fetch_messages, messages_view

app_name = MailConfig.name

urlpatterns = [
    path('', messages_view, name='messages'),
    path('fetch_messages/', fetch_messages, name='fetch_messages'),
]
