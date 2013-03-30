# -*- coding: utf-8 -*-
from django.db import models
from core.models import Node
from django.contrib import admin


class Department(Node):
    text = models.TextField(null=True, blank=True)


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'path')
admin.site.register(Department, DepartmentAdmin)


def get_node():
    return Department()
