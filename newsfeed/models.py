from django.db import models
from core.models import Node
from django.contrib import admin
import datetime


class Category(models.Model):
    title = models.CharField(max_length=255)

    def __unicode__(self):
        return self.title

    def Meta(self):
        verbose_name_plural = "categories"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
admin.site.register(Category, CategoryAdmin)


class Novelty(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=255)
    text = models.TextField()
    added = models.DateTimeField(default=datetime.datetime.now())

    def category_title(self):
        return self.category.title

    def __unicode__(self):
        return self.title

    def Meta(self):
        get_latest_by = "added"
        ordering = ['added']
        verbose_name_plural = "novelties"


class NoveltyAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'category_title', 'added')
admin.site.register(Novelty, NoveltyAdmin)


class Newsfeed(Node):
    category = models.ForeignKey(Category, null=True)

    def __unicode__(self):
        return self.title

    def get_news(self):
        return Novelty.objects.filter(category=self.category)


class NewsfeedAdmin(admin.ModelAdmin):
    list_display = ('title', 'path')
admin.site.register(Newsfeed, NewsfeedAdmin)


def get_node():
    return Newsfeed()

