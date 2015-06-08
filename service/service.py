__author__ = 'Bersik'

import logging
from model import Student
import work_database
from spyne.application import Application
from spyne.decorator import srpc, rpc
from spyne.service import ServiceBase
from spyne.protocol.soap import Soap11

from spyne.model.complex import Array
from spyne.model.primitive import Int
from spyne.model.primitive import Boolean
from spyne.util.xml import *

from spyne.server.wsgi import WsgiApplication

from wsgiref.simple_server import make_server


class CampusService(ServiceBase):

    @rpc(_returns=Boolean)
    def clear(self):
        return work_database.clear_database()

    @rpc(Student, _returns=Int)
    def add(self,student):
        return work_database.add(get_object_as_xml(student, Student, None, True))

    @rpc(_returns=Array(Student))
    def read_all(self):
        return work_database.read_all()

    @rpc(Int, _returns=Student)
    def read(self,idn):
        return work_database.read(idn)

    @rpc(Int, Student, _returns=Boolean)
    def update(self,idn, student):
        return work_database.update(idn, get_object_as_xml(student, Student, None, True))

    @rpc(Int, _returns=Boolean)
    def remove(self,idn):
        return work_database.remove(idn)


class CampusSoapServer(object):
    server_ = None

    @classmethod
    def start(cls, port=7790):
        app = Application([CampusService], 'campus',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11(),
        )

        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)

        wsgi_app = WsgiApplication(app)
        cls.server_ = make_server('127.0.0.1', port, wsgi_app)

        print 'listening to http://127.0.0.1:%d' % port
        print 'wsdl is at: http://127.0.0.1:%d/?wsdl' % port

        cls.server_.serve_forever()

    @classmethod
    def stop(cls):
        if cls.server_:
            cls.server_.shutdown()
            cls.server_.server_close()






