__author__ = 'Bersik'

from suds.client import Client as ClientSOAP

_programmer_translate_dict = {
    'name': str,
    'surname': str,
    'age': int,
    'hostel': int,
    'group': str,
    'room': int,
    'idn': int
}


def localhost_client():
    return ClientSOAP('http://127.0.0.1:7789/?wsdl', cache=None)


def student_as_dict(student):
    student_dict = {}
    for field, val in student:
        if field in _programmer_translate_dict:
            student_dict[field] = _programmer_translate_dict[field](val)
        else:
            student_dict[field] = val
    return student_dict


class Client():
    def __init__(self):
        self.client = localhost_client()

    def add(self, student):
        id = self.client.service.add(student)
        if id == -1:
            return None
        return id

    def read_all(self):
        resp = self.client.service.read_all()
        if resp:
            return resp[0]
        return None

    def read(self, id):
        student = self.client.service.read(id)
        return student

    def update(self, id, student):
        resp = self.client.service.update(id, student)
        return resp

    def remove(self, id):
        resp = self.client.service.remove(id)
        return resp

    def clear(self):
        resp = self.client.service.clear()
