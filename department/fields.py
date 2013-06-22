from django.db import models
from django import forms

from widgets import PassiveHTMLWidget


class PassiveHTMLField(models.TextField):
    def formfield(self, **kwargs):
        defaults = {
            'form_class': PassiveHTMLFormField
        }
        defaults.update(kwargs)
        return super(PassiveHTMLField, self).formfield(**defaults)


class PassiveHTMLFormField(forms.fields.Field):
    def __init__(self, *args, **kwargs):
        kwargs.update({'widget': PassiveHTMLWidget()})
        super(PassiveHTMLFormField, self).__init__(*args, **kwargs)