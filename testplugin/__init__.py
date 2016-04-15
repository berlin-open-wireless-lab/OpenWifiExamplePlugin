def addPluginRoutes(config):
    config.add_route('testplugin', '/testplugin')
    return "Testplugin"

def addJobserverTasks(app):
    @app.task
    def testPluginTask():
        print("testplugin task")
