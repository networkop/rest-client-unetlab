import unittest
from unetlab import *

USERNAME = "admin"
PASSWORD = "unl"
UNETLAB_ADDRESS = '192.168.247.20'
LAB_NAME = 'test_rest'


class UnlTests(unittest.TestCase):

    def setUp(self):
        self.unl = UnetLab(UNETLAB_ADDRESS)
        self.user = USERNAME
        self.pwd = PASSWORD
        resp = self.unl.authenticate(USERNAME, PASSWORD)
        self.assertEqual(200, resp.status_code)

    def tearDown(self):
        resp = self.unl.logout()
        self.assertEqual(200, resp.status_code)


class BasicUnlTests(UnlTests):

    def test_user_info(self):
        resp = self.unl.get_user_info()
        self.assertEqual(200, resp.status_code)

    def test_status(self):
        resp = self.unl.get_status()
        self.assertEqual(200, resp.status_code)

    def test_templates(self):
        resp = self.unl.get_templates()
        self.assertEqual(200, resp.status_code)


class BasicUnlLabTest(UnlTests):

    def test_create_lab(self):
        UnlLab().delete_lab(self.unl, LAB_NAME)
        resp = UnlLab().create_lab(self.unl, LAB_NAME)
        self.assertEqual(200, resp.status_code)

    def test_delete_lab(self):
        resp = UnlLab().delete_lab(self.unl, LAB_NAME)
        self.assertEqual(200, resp.status_code)


def main():
    unittest.main()

if __name__ == '__main__':
    main()