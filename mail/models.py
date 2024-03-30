from django.db import models


class Attachment(models.Model):
    file = models.FileField(upload_to='attachments/')

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
