__author__ = 'Bersik'


import unittest
from service import service,work_database
from client.client import Client
import multiprocessing
import time


class SoapIntegrationTest(unittest.TestCase):  # Alive database is required
    _service_process = multiprocessing.Process(target=service.CampusSoapServer.start)

    @classmethod
    def setUpClass(cls):
        cls._service_process.start()
        time.sleep(1)
        cls.client = Client()
        cls.student1 = cls.client.create_student('TestName1','TestSurname1',20,'KV-21',15,200)
        cls.student2 = cls.client.create_student('TestName2','TestSurname2',40,'KV-11',14,500)
        cls.student3 = cls.client.create_student('TestName3','TestSurname3',30,'KV-41',16,405)

        cls.student1_update = cls.client.create_student('TestName1','TestSurname1',20,'KV-41',16,209)
        cls.student2_update = cls.client.create_student('TestName2','TestSurname2',23,'KV-31',12,109)
        cls.client.clear()

    @classmethod
    def tearDownClass(cls):
        cls._service_process.terminate()

    def clear(self):
        self.client.clear()

    def equalStudent(self,dict,student):
        self.assertEquals(dict["name"],student.name)
        self.assertEquals(dict["surname"],student.surname)
        self.assertEquals(dict["age"],student.age)
        self.assertEquals(dict["group"],student.group)
        self.assertEquals(dict["hostel"],student.hostel)
        self.assertEquals(dict["room"],student.room)

    def test_1create(self):
        self.assertEqual(0, self.client.add(self.student1))
        self.assertEqual(1, self.client.add(self.student2))
        self.assertEqual(2, self.client.add(self.student3))

    def test_2read(self):
        self.equalStudent(self.student1,self.client.read(0))
        self.equalStudent(self.student2,self.client.read(1))

    def test_3update(self):
        self.assertEquals(self.client.update(0,self.student1_update),True)
        self.assertEquals(self.client.update(1,self.student2_update),True)

        self.equalStudent(self.student1_update,self.client.read(0))
        self.equalStudent(self.student2_update,self.client.read(1))

    def test_4read_all(self):
        students = self.client.read_all()
        self.assertEquals(len(students),3)
        self.equalStudent(self.student1_update,self.client.read(0))
        self.equalStudent(self.student2_update,self.client.read(1))
        self.equalStudent(self.student3,self.client.read(2))

    def test_5delete(self):
        self.assertEquals(self.client.remove(2),True)
        students = self.client.read_all()
        self.assertEquals(len(students), 2)

if __name__ == '__main__':
    unittest.main()