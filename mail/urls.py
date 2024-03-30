from django.urls import path
from mail.apps import MailConfig
from mail.views import fetch_messages

app_name = MailConfig.name

urlpatterns = [
    path('', fetch_messages, name='fetch_messages'),
]
