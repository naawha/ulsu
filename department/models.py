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
    show_rightmenu = models.BooleanField()
    rightmenu = models.TextField(null=True, blank=True)
    status = models.BooleanField()
    text = RichTextField(null=True, blank=True)

    def style_rightmenu(self):
        if self.show_rightmenu:
            return '✓'
        else:
            return ''

    def style_status(self):
        if self.status:
            return '✓'
        else:
            return ''

    def save(self, user, *args, **kwagrs):
        super(Department, self).save(*args, **kwagrs)
        if self.text:
            h = History()
            h.node = self
            h.page = self.text
            h.user = user
            h.save()


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'path','status','show_rightmenu')

    def save_model(self, request, obj, form, change):
        obj.save(request.user)


class History(models.Model):
    user = models.ForeignKey(User)
    node = models.ForeignKey(Department)
    page = PassiveHTMLField(null=True, blank=True)
    date = models.DateTimeField(default=datetime.now())

    def safe_text(self):
        return mark_safe(self.page)

    def path(self):
        return self.node.path()


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
