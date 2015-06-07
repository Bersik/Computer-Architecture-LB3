__author__ = 'Bersik'

import multiprocessing
import signal
from service.service import CampusSoapServer

soap_thread = multiprocessing.Process(target=CampusSoapServer.start)
soap_thread.start()


def sigint_handler(*_):
    if soap_thread.is_alive():
        soap_thread.terminate()


signal.signal(signal.SIGINT, sigint_handler)
signal.pause()

