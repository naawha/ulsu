# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from views import *
import re

urlpatterns = patterns(
    '',
    url(r'^$', main_page),
    url(r'^', router),

)

custom = (
    (re.compile(r'^add$'), add, 'add'),
)
