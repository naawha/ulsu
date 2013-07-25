# -*- coding: utf-8 -*-
from django.template import loader, Context, RequestContext, Template
from django.http import HttpResponse, Http404
from models import *
from core.models import Node
from django.conf import settings
from django.shortcuts import redirect


def view(request, node):
    records = Message.objects.all()
    
    t = loader.get_template("guestbook/view.html")
    c = RequestContext(request, {'node': node, 'records': records,})
    return HttpResponse(t.render(c))
    
def add_message(request, node):
    t = loader.get_template("guestbook/add_message.html")
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))

def save_message(request, node):
    if request.method == 'POST':
        dictonary = {
                'author_email':        request.POST['author'],
                'message_name':        request.POST['mname'],
                'message_text':        request.POST['mtext'],
            }
        Message.objects.create(**dictonary)
    return redirect(node.path())
    
def delete_message(request, node):
    try:
        Message.objects.filter(id=request.POST['id']).delete()
    except:
        return HttpResponse(False)
    else:
        return HttpResponse(True)
    