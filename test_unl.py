import unittest
from unetlab import *
from device import *
import time

USERNAME = "admin"
PASSWORD = "unl"
UNETLAB_ADDRESS = '192.168.247.20'
LAB_NAME = 'test_rest'
HOSTNAME = '123'
SET_COMMAND = 'conf t\r\nhostname ' + HOSTNAME
VERIFY_COMMAND = 'show run | i hostname'



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
        self.unl.delete_lab(LAB_NAME)
        resp = self.unl.create_lab(LAB_NAME).resp
        self.assertEqual(200, resp.status_code)

    def test_delete_lab(self):
        self.unl.create_lab(LAB_NAME)
        resp = self.unl.delete_lab(LAB_NAME)
        self.assertEqual(200, resp.status_code)


class BasicUnlNodeTest(UnlTests):

    def setUp(self):
        super(BasicUnlNodeTest, self).setUp()
        self.lab = self.unl.create_lab(LAB_NAME)
        self.device = Router('R0')

    def tearDown(self):
        self.lab.stop_all_nodes()
        self.lab.del_all_nodes()
        self.unl.delete_lab(LAB_NAME)
        super(BasicUnlNodeTest, self).tearDown()

    def test_create_node(self):
        resp = self.lab.create_node(self.device).resp
        self.assertEqual(201, resp.status_code)

    def test_delete_node(self):
        self.lab.create_node(self.device)
        resp = self.lab.delete_node(self.lab.get_node_id_by_name(self.device.name))
        self.assertEqual(200, resp.status_code)

    def test_create_net(self):
        resp = self.lab.create_net("DUMMY_NET").resp
        self.assertEqual(201, resp.status_code)

    def test_delete_net(self):
        self.lab.create_net("DUMMY_NET")
        resp = self.lab.delete_net(self.lab.get_net_id_by_name("DUMMY_NET"))
        self.assertEqual(200, resp.status_code)

    def test_node_config(self):
        node = self.lab.create_node(self.device)
        resp = node.get_config()
        self.assertEqual(200, resp.status_code)


class AdvancedUnlNodeTest(BasicUnlNodeTest):

    def setUp(self):
        super(AdvancedUnlNodeTest, self).setUp()
        self.device_one = Router('R1')
        self.device_two = Router('R2')

    def tearDown(self):
        super(AdvancedUnlNodeTest, self).tearDown()

    def test_connect_nodes(self):
        node_one = self.lab.create_node(self.device_one)
        node_two = self.lab.create_node(self.device_two)
        resp1, resp2 = node_one.connect_node(node_two)
        self.assertEqual(201, resp1.status_code) and self.assertEqual(201, resp2.status_code)

    def test_start_nodes(self):
        self.lab.create_node(self.device_one)
        self.lab.create_node(self.device_two)
        resp = self.lab.start_all_nodes()
        self.assertEqual(200, resp.status_code)

    def test_stop_nodes(self):
        self.lab.start_all_nodes()
        resp = self.lab.stop_all_nodes()
        self.assertEqual(200, resp.status_code)

    def test_node_wipe(self):
        pass

    #@unittest.skip("troubleshooting node start/stop")
    def test_node_import(self):
        node = self.lab.create_node(self.device)
        resp = self.lab.start_all_nodes()
        self.device.set_url(node.get_url())
        self.device.set_config(SET_COMMAND)
        result = self.device.verify_config(VERIFY_COMMAND)
        self.assertRegexpMatches(result, HOSTNAME)

    def test_node_interfaces(self):
        self.device = Router('R1')
        dev = self.lab.create_node(self.device)
        resp = dev.get_interfaces()
        self.assertEqual(200, resp.status_code)


def main():
    unittest.main()

if __name__ == '__main__':
    main()