__author__ = 'Bersik'

import mock
import unittest

from service import service,work_database,model
from client import client

class Test(unittest.TestCase):
    @mock.patch('work_database.read')
    def test_read(self,read_function):
        pass


