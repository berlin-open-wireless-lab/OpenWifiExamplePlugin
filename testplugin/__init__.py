from time import sleep

modelString = 'testplugin.models'
globalTestpluginViews = [['testplugin', 'Testplugin']]

def addPluginRoutes(config):
    config.add_route('testplugin', '/testplugin')
    config.add_route('testplugin_assign', '/testplugin/add/{uuid}')
    config.add_route('testplugin_testtask', '/testplugin/testtask')
    return "Testplugin"

def addJobserverTasks(app):
    @app.task
    def testPluginTask():
        print("testplugin task")
    @app.task
    def testLongTask():
        from openwifi.jobserver.tasks import get_sql_session
        from openwifi.models import OpenWrt
        DBSession = get_sql_session()
        devices = DBSession.query(OpenWrt)
        while True:
            print(devices[0].uuid)
            for plugin in devices[0].testPlugin:
                print(plugin.test)
            sleep(5)
        
