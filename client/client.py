__author__ = 'Bersik'



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
    from suds.client import Client
    return Client('http://127.0.0.1:7789/?wsdl', cache=None)


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
        student = self.client.service.read(str(id))
        return student

    def update(self, id, student):
        resp = self.client.service.update(id, student)
        return resp

    def remove(self, id):
        resp = self.client.service.remove(id)
        return resp

    def clear(self):
        return self.client.service.clear()

    def create_student(self,name="", surname="", age=0, group="", hostel=0, room=0):
        return {"name": name, "surname": surname, "age": age, "group": group, "hostel": hostel, "room": room}

