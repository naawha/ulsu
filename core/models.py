# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


class InheritanceCastModel(models.Model):
    """
    An abstract base class that provides a ``real_type`` FK to ContentType.

    For use in trees of inherited models, to be able to downcast
    parent instances to their child types.

    """
    real_type = models.ForeignKey(ContentType, editable=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.real_type = self._get_real_type()
        super(InheritanceCastModel, self).save(*args, **kwargs)

    def _get_real_type(self):
        return ContentType.objects.get_for_model(type(self))

    def cast(self):
        return self.real_type.get_object_for_this_type(pk=self.pk)

    class Meta:
        abstract = True


class Module(InheritanceCastModel):
    node = models.ForeignKey('Node', blank=True, null=True)
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
        return 'qwqw'


class TimetableAdmin(admin.ModelAdmin):
    list_display = ('title', 'node_name')
admin.site.register(Timetable, TimetableAdmin)




class Node(InheritanceCastModel):
    parent = models.ForeignKey('Node', blank=True, null=True, verbose_name='Родительский узел')
    node_name = models.CharField(max_length=30, verbose_name='Имя узла')
    title = models.CharField(max_length=255, verbose_name='Заголовок страницы')
    creator = models.ForeignKey(User, verbose_name='Создатель', editable=False)
    show_rightmenu = models.BooleanField(verbose_name='Отображать правое меню', help_text='В правом меню перечислены дочерние страницы')
    rightmenu = models.TextField(null=True, blank=True, verbose_name='Содержимое правого меню', help_text='Если поле пустое, правое меню сгенерируется автоматически')
    status = models.BooleanField(verbose_name='Скрыть страницу')

    def path(self):
        if self.parent is not None:
            return self.parent.path() + self.node_name + '/'
        else:
            return '/'

    def children(self):
        return Node.objects.filter(parent=self)

    def breadcrumbs(self):
        if self.parent is None:
            return [{'title': self.title, 'path': self.path()}]
        else:
            return self.parent.breadcrumbs() + [{'title': self.title, 'path': self.path()}]

    def breadcrumbs_w_last(self):
        if self.parent is None:
            return []
        else:
            return self.parent.breadcrumbs()

    def breadcrumbs_display(self):
        if self.parent is None:
            return []
        else:
            return self.parent.breadcrumbs()[1:-1]

    def modules(self):
        return [eval('m.' + str(m.real_type)) for m in Module.objects.filter(node=self)]

    def static_url(self):
        if self.parent is None:
            return '/'
        else:
            return '/get/' + str(self.id)

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

    def __unicode__(self):
        return self.path()

    def save(self, user, *args, **kwagrs):
        if not self.pk:
            self.creator = user
        super(Node, self).save(*args, **kwagrs)

class NodeAdmin(admin.ModelAdmin):
    readonly_fields = ('creator',)
    list_display = ('title', 'path')

    def save_model(self, request, obj, form, change):
        obj.save(request.user)

admin.site.register(Node, NodeAdmin)