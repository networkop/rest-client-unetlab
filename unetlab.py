from client import RestServer
import json
import device
from helpers import *

REST_SCHEMA = {
    'authenticate': '/auth/login',
    'get_user_info': '/auth',
    'logout': '/auth/logout',
    'status': '/status',
    'list_templates': '/list/templates/',
    'labs': '/labs'
}


class UnetLab(object):

    def __init__(self, address):
        self.server = RestServer(address)

    def authenticate(self, user, pwd):
        api_call = REST_SCHEMA['authenticate']
        payload = {
            "username": user,
            "password": pwd
        }
        resp = self.server.add_object(api_call, data=payload)
        self.server.set_cookies(resp.cookies)
        return resp

    def get_user_info(self):
        api_call = REST_SCHEMA['get_user_info']
        resp = self.server.get_object(api_call)
        return resp

    def logout(self):
        api_call = REST_SCHEMA['logout']
        resp = self.server.get_object(api_call)
        return resp

    def get_status(self):
        api_call = REST_SCHEMA['status']
        resp = self.server.get_object(api_call)
        return resp

    def get_templates(self):
        api_call = REST_SCHEMA['list_templates']
        resp = self.server.get_object(api_call)
        return resp


class UnlLab(object):

    def create_lab(self, unl, name):
        api_call = REST_SCHEMA['labs']
        payload = {
           "path": "/",
           "name": name,
           "version": "1"
        }
        resp = unl.server.add_object(api_call, data=payload)
        return resp

    def delete_lab(self, unl, name):
        api_call = '/labs/{lab_name}'
        api_url = api_call.format(api_call, lab_name=append_unl(name))
        resp = unl.server.del_object(api_url)
        return resp


class UnlNode(object):

    def add_node(self, dev):
        api_call = '/labs/{lab_name}/nodes'
        api_url = api_call.format(api_call, lab_name=append_unl(LAB_NAME))
        payload = dev.to_json()
        resp = self.server.add_object(api_url, data=payload)
        return resp

    def get_nodes(self):
        api_call = '/labs/{lab_name}/nodes'
        api_url = api_call.format(api_call, lab_name=append_unl(LAB_NAME))
        resp = self.server.get_object(api_url)
        return resp

    def get_node_by_name(self, node_name):
        node_dict = json.loads(self.get_nodes().content)['data']
        for node_id in node_dict:
            if node_dict[node_id]["name"] == node_name:
                return node_id
        return None

    def get_node_interfaces(self, node_id):
        api_call = '/labs/{lab_name}/nodes/{node_id}/interfaces'
        api_url = api_call.format(api_call, lab_name=append_unl(LAB_NAME), node_id=node_id)
        resp = self.server.get_object(api_url)
        return resp

    def del_node(self, node_id):
        api_call = '/labs/{lab_name}/nodes/{node_id}'
        api_url = api_call.format(api_call, lab_name =append_unl(LAB_NAME), node_id=node_id)
        resp = self.server.del_object(api_url)
        return resp

    def del_all_nodes(self):
        node_dict = json.loads(self.get_nodes().content)['data']
        for node_id in node_dict:
            self.del_node(node_id)
        return

    def add_net(self, type='bridge', name = 'NET'):
        api_call = '/labs/{lab_name}/networks'
        payload = dict()
        payload['type'] = type
        payload['name'] = name
        api_url = api_call.format(api_call, lab_name=append_unl(LAB_NAME))
        resp = self.server.add_object(api_url, data=payload)
        return resp

    def get_nets(self):
        api_call = '/labs/{lab_name}/networks'
        api_url = api_call.format(api_call, lab_name=append_unl(LAB_NAME))
        resp = self.server.get_object(api_url)
        return resp

    def get_net_by_name(self, net_name):
        nets_dict = json.loads(self.get_nets().content)['data']
        for net_id in nets_dict:
            if nets_dict[net_id]["name"] == net_name:
                return net_id
        return None

    def del_net(self, net_id):
        api_call = '/labs/{lab_name}/networks/{net_id}'
        api_url = api_call.format(api_call, lab_name=append_unl(LAB_NAME), net_id=net_id)
        resp = self.server.del_object(api_url)
        return resp

    def del_all_nets(self):
        nets_dict = json.loads(self.get_nets().content)['data']
        for node_id in nets_dict:
            self.del_net(node_id)
        return

    def connect_interface(self, node_id, net_id):
        api_call = '/labs/{lab_name}/nodes/{node_id}/interfaces'
        api_method = 'PUT'
        api_url = api_call.format(api_call, lab_name=append_unl(LAB_NAME), node_id = node_id)
        payload = {"0": net_id}
        resp = self.server.send_request(api_method, api_url, data=payload)
        return resp

    def connect_nodes(self, node1, node2):
        net_name = "ONE"
        self.add_net(name=net_name)
        net_id = self.get_net_by_name(net_name)
        node1_id = self.get_node_by_name(node1)
        node2_id = self.get_node_by_name(node2)
        resp1 = self.connect_interface(node1_id, net_id)
        resp2 = self.connect_interface(node2_id, net_id)
        return resp1, resp2

    def start_all_nodes(self):
        api_call = '/labs/{lab_name}/nodes/start'
        api_url = api_call.format(api_call, lab_name=append_unl(LAB_NAME))
        resp = self.server.get_object(api_url)
        return resp


def main():
    pass


if __name__ == '__main__':
    main()

