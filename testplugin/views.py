from pyramid.view import view_config
from celery import signature

@view_config(route_name='testplugin', renderer='templates/test.jinja2', layout='base', permission='view')
def testplugin(request):

    # run a test Task
    testTask = signature('testplugin.testPluginTask')
    testTask.delay()

    return {}
