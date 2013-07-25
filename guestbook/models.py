# -*- coding: utf-8 -*-
from symbol import return_stmt
from django.db import models
from core.models import Node
from django.contrib import admin
from ckeditor.fields import RichTextField
from datetime import datetime
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

def get_node():
    return Guestbook()


class Guestbook(Node):
    text = RichTextField(null=True, blank=True, verbose_name='Содержимое страницы')

    class Meta:
        verbose_name='guestbook'
        verbose_name_plural='Гостевая книга'


class GuestbookAdmin(admin.ModelAdmin):
    list_display = ('title', 'path','status','show_rightmenu')

    def save_model(self, request, obj, form, change):
        obj.save(request.user)
    
class Message(models.Model):
    author_email = models.CharField(max_length=255)
    message_name = models.CharField(max_length=255)
    message_text = models.TextField()
    message_date = models.DateTimeField(default=datetime.now())
    message_comment = models.TextField(blank=True, null=True)
    class Meta:
        ordering=['-message_date']
    
class MessageAdmin(admin.ModelAdmin):
    list_display = ('author_email', 'message_name', 'message_text', 'message_date', 'message_comment',)

admin.site.register(Guestbook, GuestbookAdmin)
admin.site.register(Message, MessageAdmin)

