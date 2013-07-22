# -*- coding: utf-8 -*-
from symbol import return_stmt
from django.db import models
from core.models import Node
from django.contrib import admin
from ckeditor.fields import RichTextField
from datetime import datetime
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from fields import PassiveHTMLField


def get_node():
    return Department()


class Department(Node):
    text = RichTextField(null=True, blank=True, verbose_name='Содержимое страницы')

    def save(self, user, *args, **kwagrs):
        super(Department, self).save(user, *args, **kwagrs)
        if self.text:
            h = History()
            h.node = self
            h.page = self.text
            h.user = user
            h.save()

    class Meta:
        verbose_name='department'
        verbose_name_plural='Департаменты'


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'path','status','show_rightmenu')

    def save_model(self, request, obj, form, change):
        obj.save(request.user)


class History(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', help_text='Пользователь, который внёс изменения')
    node = models.ForeignKey(Department, verbose_name='Департамент', help_text='Текущий адрес изменённого департамента')
    page = PassiveHTMLField(null=True, blank=True, verbose_name='Содержимое страницы')
    date = models.DateTimeField(default=datetime.now(), verbose_name='Дата изменения')

    def safe_text(self):
        return mark_safe(self.page)

    def path(self):
        return self.node.path()

    class Meta:
        verbose_name='История'
        verbose_name_plural='История'

class HistoryAdmin(admin.ModelAdmin):
    list_display = ('path', 'date', 'user')
    readonly_fields = ('user', 'node', 'date',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        return False

admin.site.register(Department, DepartmentAdmin)
admin.site.register(History, HistoryAdmin)
