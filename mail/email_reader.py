import imaplib
import email
from email.header import decode_header
from mail.models import EmailMessage


class EmailReader:
    def __init__(self, email_address, password):
        self.email_address = email_address
        self.password = password

    def fetch_email_messages(self):
        # Connect to IMAP server
        mail = imaplib.IMAP4_SSL('imap.yandex.ru')
        mail.login(self.email_address, self.password)
        mail.select('inbox')

        # Search for all emails
        result, data = mail.search(None, 'ALL')
        messages = []
        for num in data[0].split():
            result, data = mail.fetch(num, '(RFC822)')
            raw_email = data[0][1]
            email_message = email.message_from_bytes(raw_email)
            subject = self.decode_header(email_message['Subject'])[0][0]
            sent_date = email_message['Date']
            received_date = email_message['Received']
            body = self.get_email_body(email_message)
            attachments = self.get_attachments(email_message)
            messages.append({
                'subject': subject,
                'sent_date': sent_date,
                'received_date': received_date,
                'body': body,
                'attachments': attachments
            })
        mail.logout()
        return messages

    @staticmethod
    def decode_header(self, header):
        return decode_header(header)

    @staticmethod
    def get_email_body(self, email_message):
        body = ''
        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                try:
                    body += part.get_payload(decode=True).decode()
                except:
                    pass
        else:
            body = email_message.get_payload(decode=True).decode()
        return body

    @staticmethod
    def get_attachments(self, email_message):
        attachments = []
        for part in email_message.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            filename = part.get_filename()
            if filename:
                attachment = {
                    'filename': filename,
                    'file': part.get_payload(decode=True)
                }
                attachments.append(attachment)
        return attachments
