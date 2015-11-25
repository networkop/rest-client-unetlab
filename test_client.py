import unittest
from client import *

USERNAME = "admin"
PASSWORD = "unl"


class UnlTests(unittest.TestCase):

    def test_auth(self):
        unl = UnlLabs()
        resp = unl.authenticate(USERNAME, PASSWORD)
        self.assertEqual(200, resp.status_code)

    def test_del_lab(self):
        unl = UnlLabs()
        unl.authenticate(USERNAME, PASSWORD)
        unl.create_lab()
        resp = unl.delete_lab()
        self.assertEqual(200, resp.status_code)

    def test_del_lab(self):
        unl = UnlLabs()
        unl.authenticate(USERNAME, PASSWORD)
        unl.create_lab()
        resp = unl.delete_lab()
        self.assertEqual(200, resp.status_code)

    def test_add_device(self):
        unl = UnlLabs()
        unl.authenticate(USERNAME, PASSWORD)
        unl.create_lab()
        r1 = device.Router('R1')
        resp = unl.add_node(r1)
        self.assertEqual(201, resp.status_code)

    def test_connect_devices(self):
        unl = UnlLabs()
        unl.authenticate(USERNAME, PASSWORD)
        unl.create_lab()
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