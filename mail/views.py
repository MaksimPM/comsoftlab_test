import imaplib
import os
import email
from datetime import datetime
from dateutil import parser
from django.conf import settings
from django.shortcuts import render
from mail.models import Message, Attachment
import re
from bs4 import BeautifulSoup


def decode_sender(encoded_sender):
    if not encoded_sender:
        return ""

    if isinstance(encoded_sender, bytes):
        try:
            decoded_sender = encoded_sender.decode('utf-8')
            return decoded_sender
        except UnicodeDecodeError:
            pass

    return encoded_sender


def fetch_messages(request):
    email_host = imaplib.IMAP4_SSL(os.getenv('EMAIL_HOST'))
    email_username = os.getenv('EMAIL_HOST_USER')
    email_password = os.getenv('EMAIL_HOST_PASSWORD')
    email_host.login(email_username, email_password)

    email_host.select('"INBOX"')
    status, messages = email_host.search(None, 'UNSEEN')

    new_messages = []
    current_time = datetime.now()

    for message_id in messages[0].split()[::-1]:
        _, msg = email_host.fetch(message_id, "(RFC822)")
        m = email.message_from_bytes(msg[0][1])

        subject_header = m['Subject']
        decoded_subject = email.header.decode_header(subject_header)
        subject_tuple = decoded_subject[0]
        if isinstance(subject_tuple[0], bytes):
            subject = subject_tuple[0].decode(subject_tuple[1] or 'utf-8')
        else:
            subject = subject_tuple[0]

        sender = m['From']
        sender_email = re.findall(r'<([^>]+)>', sender)[0] if re.findall(r'<([^>]+)>', sender) else sender
        sender_email = decode_sender(sender_email)

        sent_date_raw = m['Date']
        sent_date = parser.parse(sent_date_raw)

        body = ""
        attachments = []

        if m.is_multipart():
            for part in m.walk():
                content_type = part.get_content_type()
                if "text/html" in content_type:
                    html_content = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8')
                    soup = BeautifulSoup(html_content, 'html.parser')
                    body = soup.get_text(separator="\n")
                    break
                elif "text/plain" in content_type:
                    body = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8')
                elif "multipart" not in content_type:
                    filename = part.get_filename()
                    if filename:
                        filename_tuple = email.header.decode_header(filename)[0]
                        if isinstance(filename_tuple[0], bytes):
                            filename = filename_tuple[0].decode(filename_tuple[1] or 'utf-8')
                        else:
                            filename = filename_tuple[0]
                        attachment_data = part.get_payload(decode=True)
                        attachment_path = os.path.join(settings.MEDIA_ROOT, 'attachments', filename)
                        with open(attachment_path, 'wb') as file:
                            file.write(attachment_data)
                        attachment = Attachment.objects.create(filename=filename, file=filename)
                        attachments.append(attachment)

        if not body:
            for part in m.walk():
                content_type = part.get_content_type()
                if "text/plain" in content_type:
                    body = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8')
                    break

        try:
            message_obj = Message.objects.get(subject=subject, sent_date=sent_date)
            print("Сообщение уже существует:", message_obj)
        except Message.DoesNotExist:
            message_obj = Message.objects.create(subject=subject, sent_date=sent_date, received_date=current_time,
                                                 body=body)
            message_obj.attachments.set(attachments)
            new_messages.append({
                'subject': subject,
                'sender': sender_email,
                'sent_date': sent_date.strftime('%Y-%m-%d %H:%M:%S'),
                'received_date': current_time.strftime('%Y-%m-%d %H:%M:%S'),
                'body': body,
                'attachments': [attachment.filename for attachment in attachments],
            })

    email_host.logout()

    context = {'messages': new_messages}
    return render(request, 'index.html', context)
