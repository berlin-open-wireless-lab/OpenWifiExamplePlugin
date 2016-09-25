modelString = 'testplugin.models'
globalTestpluginViews = [['testplugin', 'Testplugin']]

def addPluginRoutes(config):
    config.add_route('testplugin', '/testplugin')
    config.add_route('testplugin_assign', '/testplugin/add/{uuid}')
    return "Testplugin"

def testOnDeviceRegister(uuid):
    from openwifi.models import OpenWrt, DBSession
    device = DBSession.query(OpenWrt).get(uuid)
    print("testplugin " + str(device))

def addJobserverTasks(app):
    @app.task
    def testPluginTask():
        print("testplugin task")
