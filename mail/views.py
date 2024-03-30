import imaplib
import os
import email
from datetime import datetime
from dateutil import parser
from django.shortcuts import render
from .models import Message, Attachment
import base64
import re

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
        subject = decoded_subject[0][0].decode(decoded_subject[0][1] or 'utf-8')
        if isinstance(subject, bytes):
            subject = subject.decode(decoded_subject[0][1])

        sender = m['From']
        sender_email = re.findall(r'<([^>]+)>', sender)[0] if re.findall(r'<([^>]+)>', sender) else sender
        sender_email = decode_sender(sender_email)

        sent_date_raw = m['Date']
        sent_date = parser.parse(sent_date_raw)

        body = ""
        attachments = []

        if m.is_multipart():
            for part in m.walk():
                if part.get_content_maintype() == 'multipart': continue
                filename = part.get_filename()
                if not filename: continue
                attachment_data = part.get_payload(decode=True)
                attachment_data_base64 = base64.b64encode(attachment_data).decode('utf-8')
                attachment = Attachment.objects.create(file=attachment_data_base64)
                attachments.append(attachment)
        else:
            content = m.get_payload(decode=True)
            body = content.decode("utf-8")

        try:
            message_obj = Message.objects.get(subject=subject, sent_date=sent_date)
            print("Message already exists:", message_obj)
        except Message.DoesNotExist:
            message_obj = Message.objects.create(subject=subject, sent_date=sent_date, received_date=current_time,
                                                 body=body)
            message_obj.attachments.set(attachments)
            new_messages.append({
                'subject': subject,
                'sender': sender_email,
                'sent_date': sent_date.strftime('%Y-%m-%d %H:%M:%S'),
                'body': body,
                'attachments': [attachment.file.url for attachment in attachments],
            })

    email_host.logout()

    context = {'messages': new_messages}
    return render(request, 'index.html', context)




