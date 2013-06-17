# -*- coding: utf-8 -*-
from django.template import loader, Context, RequestContext, Template
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from models import *
from django.conf import settings
import re
import json
for i in settings.CUSTOM_APPS:
    exec 'from ' + i['type'] + ' import urls as ' + i['type'] + '_urls, models as ' + i['type'] + '_models'


index_node = Node.objects.filter(parent=None)[:1]


def main_page(request):
    node = index_node
    node.title = 'Новости университета'
    t = loader.get_template("index.html")
    c = RequestContext(request, {'node': node})
    return HttpResponse(t.render(c))


def recousive_check(chunks, parent=index_node):
    try:
        pass
        node = Node.objects.get(node_name=chunks[0], parent=parent)
    except Node.DoesNotExist:
        return parent, '/'.join(chunks)
    else:
        if len(chunks) > 1:
            return recousive_check(chunks[1:], node)
        else:
            return node, "/"


def router(request):
    path = [i for i in request.path.split("/") if i != '']
    node, path = recousive_check(path)
    if node == index_node:
        u = custom
    else:
        u = eval(str(node.real_type) + '_urls.urls') + custom
        node = eval('node.' + str(node.real_type))
    for p in u:
        if p[0].match(path):
            return p[1](request, node)
    raise Http404


def add(request, node):
    e = []
    data = {}
    if request.method == 'POST':
        if request.POST['type'] in [i['type'] for i in settings.CUSTOM_APPS]:
            if request.POST['node_name'] not in [i.node_name for i in node.children()]:
                n = eval(request.POST['type'] + '_models.get_node()')
                n.node_name = request.POST['node_name']
                n.title = request.POST['title']
                n.parent = node
                n.creator = request.user
                n.save()
                return redirect(n.path() + 'edit')
            else:
                data = dict(request.POST)
                data['node_name'] = ''
                e.append('Страница с таким именем уже существует. Выберите другое имя.')
        else:
            data = request.POST
            e.append('Произошла внутренняя ошибка сервера. Обратитесь за помощью к администратору сайта по электронной почте webmaster@ulsu.ru.')
    apps = settings.CUSTOM_APPS
    t = loader.get_template("core/add.html")
    c = RequestContext(request, {
        'node': node,
        'apps': apps,
        'title': 'Создание нового компонента',
        'mode': 'add',
        'data': data,
        'e': e
    })
    return HttpResponse(t.render(c))



def branch(parent=None):
    leafs = Node.objects.filter(parent=parent)
    if leafs:
        a = []
        for l in leafs:
            o = {'name': l.node_name, 'data': l.title, 'attr': {'id': 'node_' + str(l.id)}}
            o['attr']['rel'] = l.real_type.name if parent != None else 'root'
            b = branch(l)
            if b is not None:
                o['children'] = b
            a.append(o)
        return a
    else:
        return None




@csrf_exempt
def node_tree(request):
    if request.method == 'POST':
        return HttpResponse(json.dumps(branch()))

    t = loader.get_template("admin/node_tree.html")
    c = RequestContext(request, {'title': 'Редактирование дерева', 'app_label': 'core', 'node': request})
    return HttpResponse(t.render(c))

custom = (
    (re.compile(r'^add$'), add, 'add'),
)