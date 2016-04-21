modelString = 'testplugin.models'
globalTestpluginViews = [['testplugin', 'Testplugin']]

def addPluginRoutes(config):
    config.add_route('testplugin', '/testplugin')
    config.add_route('testplugin_assign', '/testplugin/add/{uuid}')
    return "Testplugin"

def addJobserverTasks(app):
    @app.task
    def testPluginTask():
        print("testplugin task")
