# -*- coding: utf-8 -*-
from symbol import return_stmt
from django.db import models
from core.models import Node
from django.contrib import admin
from ckeditor.fields import RichTextField
from datetime import datetime
from django.contrib.auth.models import User


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
        if self.pk:
            h = History()
            h.node = self
            h.page = self.text
            h.user = user
            h.save()
        super(Department, self).save(*args, **kwagrs)

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'path','status','show_rightmenu')

def get_node():
    return Department()

class History(models.Model):
    user = models.ForeignKey(User)
    node = models.ForeignKey(Department)
    page = models.TextField(null=True, blank=True)
    date = models.DateTimeField(default=datetime.now())

class HistoryAdmin(admin.ModelAdmin):
    list_display = ('page', 'date')

admin.site.register(Department, DepartmentAdmin)
admin.site.register(History, HistoryAdmin)
