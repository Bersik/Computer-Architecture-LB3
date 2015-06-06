__author__ = 'Bersik'

import logging
from model import Student
import work_database
from spyne.application import Application
from spyne.decorator import srpc, rpc
from spyne.service import ServiceBase
from spyne.protocol.soap import Soap11

from spyne.model.complex import Iterable, Array
from spyne.model.primitive import UnsignedInteger, AnyXml, Int
from spyne.model.primitive import String, Boolean
from spyne.util.xml import *

from spyne.server.wsgi import WsgiApplication

from wsgiref.simple_server import make_server


class CampusService(ServiceBase):
    @srpc(String, UnsignedInteger, _returns=Iterable(String))
    def say_hello(name, times):
        for i in xrange(times):
            yield 'Hello, %s' % name

    @rpc(_returns=Boolean)
    def clear(self):
        return work_database.clear_database()

    @srpc(Student, _returns=Int)
    def add(student):
        return work_database.add(get_object_as_xml(student, Student, None, True))
        # return get_xml_as_object(work_database.add(get_object_as_xml(student,Student,None,True)),Student)

    @rpc(_returns=Array(Student))
    def read_all(self):
        return work_database.read_all()

    @srpc(Int, _returns=Student)
    def read(idn):
        return work_database.read(idn)

    @srpc(Int, Student, _returns=Boolean)
    def update(idn, student):
        return work_database.update(idn, get_object_as_xml(student, Student, None, True))

    @srpc(Int, _returns=Boolean)
    def remove(idn):
        return work_database.remove(idn)


class CampusSoapServer(object):
    server_ = None

    @classmethod
    def start(cls, port=7789):
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
            cls._server.shutdown()
            cls._server.server_close()






