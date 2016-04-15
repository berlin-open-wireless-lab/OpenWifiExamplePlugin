from pyramid.view import view_config

@view_config(route_name='testplugin', renderer='templates/test.jinja2', layout='base', permission='view')
def testplugin(request):
    return {}
