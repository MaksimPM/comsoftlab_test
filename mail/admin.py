from django.contrib import admin

from mail.models import Attachment, Message

admin.site.register(Message)
admin.site.register(Attachment)
