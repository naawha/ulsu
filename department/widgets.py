from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode


class PassiveHTMLWidget(forms.Textarea):
    def render(self, name, value, attrs={}):
        return mark_safe(render_to_string(
            'department/PassiveHTMLWidget.html', {
                'value': force_unicode(value)
            })
        )
