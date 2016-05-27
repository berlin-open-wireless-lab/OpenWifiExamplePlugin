from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from celery import signature

from openwifi.models import (DBSession,
                             OpenWrt)

from .models import TestPluginClass

import string
import random

@view_config(route_name='testplugin', renderer='templates/test.jinja2', layout='base', permission='view')
def testplugin(request):

    # run a test Task
    #testTask = signature('testplugin.testPluginTask')
    #testTask.delay()
    
    items = []
    devices = DBSession.query(OpenWrt)

    for device in devices:
        dev_info = {}
        dev_info['uuid']=str(device.uuid)
        dev_info['tags']=[]
        for tag in device.testPlugin:
            dev_info['tags'].append(tag.test)
        items.append(dev_info)

    return {'items' : items,
            'table_fields' : ['uuid', 'tags'],
            'idfield': 'uuid'
            }

@view_config(route_name='testplugin_assign', renderer='templates/testAssign.jinja2', layout='base', permission='view')
def testplugin_assign(request):
    if request.POST:
        uuid = request.matchdict['uuid']
        device = DBSession.query(OpenWrt).get(uuid)
        tag_text = request.POST.dict_of_lists()['tag'][0]
        new_tag = TestPluginClass(tag_text, id_generator())
        DBSession.add(new_tag)
        device.testPlugin.append(new_tag)
        return HTTPFound(location=request.route_url('testplugin'))
    return {}

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
