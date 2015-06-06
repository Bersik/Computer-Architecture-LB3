from spyne.util.xml import get_xml_as_object

__author__ = 'Bersik'

from lxml import etree
from dbxml import *
from model import Student
import os

collection_name = "service/db.dbxml"


def create_database():
    if not (os.path.exists(collection_name) and os.path.isfile(collection_name)):
        mgr = XmlManager()
        mgr.createContainer(collection_name)


def check_database(function):
    if not os.path.isfile(collection_name):
        create_database()
    return function


@check_database
def inc_id():
    global doc
    mgr = XmlManager()
    uc = mgr.createUpdateContext()
    container = mgr.openContainer(collection_name)

    try:
        doc = container.getDocument("idn")
    except:
        container.putDocument(r"idn", "<idn>1</idn>", uc)
        return 0

    try:
        tree = etree.fromstring(doc.getContent())
        idn = int(tree.text)
        doc.setContent("<idn>%d</idn>" % (idn + 1))
        container.updateDocument(doc, uc)
        return idn
    except:
        return -1


@check_database
def add(student):
    id = inc_id()
    mgr = XmlManager()
    container = mgr.openContainer(collection_name)
    uc = mgr.createUpdateContext()
    if -1 != id:
        student.attrib["idn"] = str(id)
        std = etree.tostring(student)
        container.putDocument("student_%d" % id, std, uc)
    return id


@check_database
def read_all():
    mgr = XmlManager()
    container = mgr.openContainer(collection_name)
    qc = mgr.createQueryContext()
    results = mgr.query("collection('%s')/Student" % collection_name, qc)
    results.reset()
    students = []
    for value in results:
        students.append(get_xml_as_object(etree.fromstring(value.asString()), Student))
    return students


@check_database
def read(idn):
    mgr = XmlManager()
    uc = mgr.createUpdateContext()
    container = mgr.openContainer(collection_name)
    try:
        doc = container.getDocument("student_%d" % int(idn))
        return get_xml_as_object(etree.fromstring(doc.getContent()), Student)
    except:
        return NULL_POINTER


@check_database
def update(idn, student):
    mgr = XmlManager()
    try:
        container = mgr.openContainer(collection_name)
        uc = mgr.createUpdateContext()
        document = container.getDocument("student_%d" % idn)
        student.attrib["idn"] = str(idn)
        document.setContent(etree.tostring(student))
        container.updateDocument(document, uc)
        return True
    except:
        return False


@check_database
def remove(idn):
    mgr = XmlManager()
    container = mgr.openContainer(collection_name)
    uc = mgr.createUpdateContext()
    try:
        container.deleteDocument("student_%d" % idn, uc)
    except:
        return False
    return True


def remove_database():
    if (os.path.exists(collection_name) and os.path.isfile(collection_name)):
        os.remove(collection_name)


def clear_database():
    remove_database()
    create_database()
    return True
