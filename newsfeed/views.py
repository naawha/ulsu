# -*- coding: utf-8 -*-
from django.template import loader, Context, RequestContext, Template
from django.http import HttpResponse, Http404
from models import *
from core.models import Node
from django.conf import settings


def view(request, node):
    t = loader.get_template("newsfeed/view.html")
    c = RequestContext(request, {'node': node})
    return HttpResponse(t.render(c))


def edit(request, node):
    node.title = 'Редактирование новостей'
    t = loader.get_template("newsfeed/view.html")
    c = RequestContext(request, {'node': node, 'mode': 'edit'})
    return HttpResponse(t.render(c))

