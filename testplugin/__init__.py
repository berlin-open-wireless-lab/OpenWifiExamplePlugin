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

from openwifi.communication import ClassProperty, OpenWifiCommunication
import os.path
from pyuci import Uci
from openwifi.utils import diffChanged

class ExampleTextFileCommunication(OpenWifiCommunication):
    @ClassProperty
    @classmethod
    def string_identifier_list(self):
        return ['EXAMPLE_PLUGIN_FILE']

    def get_config(device, DBSession):
        file_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(file_dir, str(device.uuid)+".txt")
        print(filepath)
        try:
            if os.path.exists(filepath):
                newConf = open(filepath).read()
            else:
                newConf = ""

            if device.configured:

                newUci = Uci()
                newUci.load_tree(newConf)

                oldUci = Uci()
                oldUci.load_tree(device.configuration)

                diff = oldUci.diff(newUci)

                if diffChanged(diff):
                    device.append_diff(diff, DBSession, "download: ")
                    device.configuration = newConf
            else:
                device.configuration = newConf
                device.configured = True

            DBSession.commit()
            DBSession.close()
            return True
        except Exception as thrownexpt:
            print(thrownexpt)
            device.configured = False
            DBSession.commit()
            DBSession.close()
            return False

    def update_config(device, DBSession):
        file_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(file_dir, str(device.uuid)+".txt")
        print(filepath)
        if os.path.exists(filepath):
            cur_conf = open(filepath).read()
        else:
            cur_conf = "{}"

        new_configuration = Uci()
        new_configuration.load_tree(device.configuration)

        cur_configuration = Uci()
        cur_configuration.load_tree(cur_conf)
        conf_diff = cur_configuration.diff(new_configuration)
        changed = diffChanged(conf_diff)

        if changed:
            device.append_diff(conf_diff, DBSession, "upload: ")
        
        print(device.configuration)
        print("going to write file")
        open(filepath, 'w').write(device.configuration)
        print("wrote to file")

        DBSession.commit()
        DBSession.close()

    def update_status(device, redisDB):
        pass

    def update_sshkeys(device, DBSession):
        file_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(file_dir, str(device.uuid)+"_keys"+".txt")

        keys = ""
        for sshkey in openwrt.ssh_keys:
            keys = keys+'#'+sshkey.comment+'\n'
            keys = keys+sshkey.key+'\n'

        open(filepath, 'w').write(keys)

    def exec_on_device(device, DBSession, cmd, prms):
        return "file example communication"
