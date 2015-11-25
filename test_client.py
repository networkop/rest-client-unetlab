import unittest
import device
from client import *

USERNAME = "admin"
PASSWORD = "unl"
LAB_NAME = 'test_rest'

class UnlTests(unittest.TestCase):

    def test_auth(self):
        unl = UnetLab()
        resp = unl.authenticate(USERNAME, PASSWORD)
        self.assertEqual(200, resp.status_code)

    def test_del_lab(self):
        unl = UnetLab()
        unl.authenticate(USERNAME, PASSWORD)
        unl.create_lab(LAB_NAME)
        resp = unl.delete_lab(LAB_NAME)
        self.assertEqual(200, resp.status_code)

    def test_del_lab(self):
        unl = UnetLab()
        unl.authenticate(USERNAME, PASSWORD)
        unl.create_lab(LAB_NAME)
        resp = unl.delete_lab(LAB_NAME)
        self.assertEqual(200, resp.status_code)

    def test_add_device(self):
        unl = UnetLab()
        unl.authenticate(USERNAME, PASSWORD)
        unl.create_lab(LAB_NAME)
        r1 = device.Router('R1')
        resp = unl.add_node(r1)
        self.assertEqual(201, resp.status_code)

    def test_connect_devices(self):
        unl = UnetLab()
        unl.authenticate(USERNAME, PASSWORD)
        unl.create_lab(LAB_NAME)
        r1 = device.Router('R1')
        r2 = device.Router('R2')
        unl.add_node(r1)
        unl.add_node(r2)
        resp1, resp2 = unl.connect_nodes("R1", "R2")
        self.assertEqual(201, resp1.status_code)
        self.assertEqual(201, resp2.status_code)

def main():
    unittest.main()

if __name__ == '__main__':
    main()