from django.db import models


class EmailAccount(models.Model):
    email = models.EmailField(verbose_name='описание')
    password = models.CharField(max_length=100, verbose_name='password')

    class Meta:
        verbose_name = 'аккаунт'
        verbose_name_plural = 'аккаунты'


class Attachment(models.Model):
    file = models.FileField(upload_to='attachments/')

    class Meta:
        verbose_name = 'вложение'
        verbose_name_plural = 'вложения'


class EmailMessage(models.Model):
    subject = models.CharField(max_length=255, verbose_name='заголовок')
    sent_date = models.DateTimeField(verbose_name='дата отправки')
    received_date = models.DateTimeField(verbose_name='дата получения')
    body = models.TextField(verbose_name='текст письма')
    attachments = models.ManyToManyField(Attachment)

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'
