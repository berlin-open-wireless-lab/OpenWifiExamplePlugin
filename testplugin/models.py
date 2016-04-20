from openwifi.models import (Base, 
                             GUID
                             )
from sqlalchemy import (
        Column,
        Text,
        Table,
        ForeignKey
        )
from sqlalchemy.orm import (
        backref,
        relationship
        )

TestPluginAssociationTable = Table('testPlugin_Association', Base.metadata,
        Column('testPlugin_id', Text, ForeignKey('testPlugin.id')),
        Column('openwrt_id', GUID, ForeignKey('openwrt.uuid')))

class TestPluginClass(Base):
    __tablename__ = 'testPlugin'
    test = Column(Text)
    id = Column(Text, primary_key=True)
    openwrts = relationship("OpenWrt",secondary=TestPluginAssociationTable,backref="testPlugin")

    def __init__(self, test, id):
        self.test = test
        self.id = id
