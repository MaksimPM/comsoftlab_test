import imaplib
import email
from email.header import decode_header
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render

from .models import EmailMessage, Attachment


def messages_view(request):
    return render(request, 'index.html')


def fetch_messages(request):
    # Извлечение настроек подключения к почтовому серверу из settings.py
    email_host = settings.EMAIL_HOST
    email_port = settings.EMAIL_PORT
    email_username = settings.EMAIL_HOST_USER
    email_password = settings.EMAIL_HOST_PASSWORD

    # Подключение к серверу
    mail = imaplib.IMAP4_SSL(email_host, email_port)
    mail.login(email_username, email_password)
    mail.select('inbox')

    # Поиск писем
    status, data = mail.search(None, 'ALL')
    message_ids = data[0].split()

    # Прогресс чтения сообщений
    total_messages = len(message_ids)
    processed_messages = 0
    progress = 0

    # Чтение каждого письма
    for message_id in message_ids:
        status, data = mail.fetch(message_id, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email)

        subject = decode_header(email_message['Subject'])[0][0]
        if isinstance(subject, bytes):
            subject = subject.decode()

        sent_date = email_message['Date']
        received_date = email.utils.parsedate_to_datetime(sent_date)

        body = ""
        attachments = []

        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                if "plain" in content_type:
                    body = part.get_payload(decode=True).decode()
                elif "attachment" in content_type:
                    filename = part.get_filename()
                    attachment = part.get_payload(decode=True)
                    attachments.append(attachment)

            # Сохранение вложений в базу данных
            for attachment in attachments:
                Attachment.objects.create(file=attachment)

        # Сохранение сообщения в базу данных
        email_message_obj = EmailMessage.objects.create(
            subject=subject,
            sent_date=sent_date,
            received_date=received_date,
            body=body
        )

        email_message_obj.attachments.set(Attachment.objects.all())

        # Обновление прогресса
        processed_messages += 1
        progress = int((processed_messages / total_messages) * 100)

    # Закрытие соединения
    mail.logout()

    return JsonResponse({'progress': progress})

