from setuptools import setup, find_packages

setup(
    name='Testplugin',
    version="0.1",
    description="Testplugin for OpenWifi",
    author="Johannes Wegener",
    install_requires=["OpenWifi"],
    entry_points="""
    [OpenWifi.plugin]
    addPluginRoutes=testplugin:addPluginRoutes
    addJobserverTasks=testplugin:addJobserverTasks
    models=testplugin:modelString
    globalPluginViews=testplugin:globalTestpluginViews
    onDeviceRegister=testplugin:testOnDeviceRegister
    communication=testplugin:ExampleTextFileCommunication
    """,
    packages=find_packages(),
    include_package_data=True,
)
