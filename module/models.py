from django.db import models
from django.contrib import admin
from views import timetable_render
import datetime


class Module('core.models.InheritanceCastModel'):
    node = models.ForeignKey('core.models.Node', blank=True, null=True)
    title = models.CharField(max_length=255)
    display = models.BooleanField(default=False)

    def node_name(self):
        return self.node.path()

    def __unicode__(self):
        return self.title


class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'node_name')

admin.site.register(Module, ModuleAdmin)


class Html(Module):
    inner_html = models.TextField()

    def data(self):
        return self.inner_html


class HtmlAdmin(admin.ModelAdmin):
    list_display = ('title', 'node_name')
admin.site.register(Html, HtmlAdmin)


class Timetable(Module):

    def data(self):
        return timetable_render


class TimetableAdmin(admin.ModelAdmin):
    list_display = ('title', 'node_name')
admin.site.register(Timetable, TimetableAdmin)

