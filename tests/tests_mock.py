__author__ = 'Bersik'

import threading
import unittest
import mock
import time
from client.client import Client
from client import client


class SoapConnectionTest(unittest.TestCase):
    def test_add(self):
        student1 = Client.create_student('TestName1', 'TestSurname1', 20, 'KV-41', 16, 209)

        self._connection_test(
            test_method_name='service.work_database.add',
            expected_res=0,
            method_call=lambda client_: client_.add(student1),
            method_pos_params=(0, ),
        )

    def test_update(self):
        student1_update = Client.create_student('TestName1', 'TestSurname1', 20, 'KV-41', 16, 209)

        self._connection_test(
            test_method_name='service.work_database.update',
            expected_res=True,
            method_call=lambda client_: client_.update(0, student1_update),
            method_pos_params=(0, ),
        )

    def test_read(self):
        student1 = Client.create_student('TestName1', 'TestSurname1', 20, 'KV-21', 15, 200)

        self._connection_test(
            test_method_name='service.work_database.read',
            expected_res=student1,
            method_call=lambda client_: client.student_as_dict(client_.read(0)),
            method_pos_params=(0, )
        )

    def test_delete(self):
        self._connection_test(
            test_method_name='service.work_database.remove',
            expected_res=True,
            method_call=lambda client: client.remove(0),
            method_pos_params=(0, )
        )

    def _connection_test(self, test_method_name, expected_res, method_call, method_pos_params=(), method_kw_params={}):
        from service.service import CampusSoapServer

        with mock.patch(test_method_name, return_value=expected_res) as method_mock:
            stop = threading.Event()
            method_result = {}

            def _stop_server():
                stop.wait()
                CampusSoapServer.stop()

            def _test_client():
                time.sleep(1)
                try:
                    client = Client()
                    method_result['result'] = method_call(client)
                finally:
                    stop.set()

            client_tester = threading.Thread(target=_test_client)
            server_stopper = threading.Thread(target=_stop_server)
            server_stopper.start()
            client_tester.start()
            CampusSoapServer.start()
            self.assertEqual(expected_res, method_result['result'])
