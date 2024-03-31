from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Attachment(models.Model):
    filename = models.CharField(max_length=500, **NULLABLE)
    file = models.FileField(upload_to='attachments', **NULLABLE)

    def __str__(self):
        return self.filename

    class Meta:
        verbose_name = 'вложение'
        verbose_name_plural = 'вложения'


class Message(models.Model):
    subject = models.CharField(max_length=1000, verbose_name='заголовок')
    sent_date = models.DateTimeField(verbose_name='дата отправки')
    received_date = models.DateTimeField(verbose_name='дата получения')
    body = models.TextField(verbose_name='текст письма')
    attachments = models.ManyToManyField(Attachment)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'
