from client import RestServer
#from device import Router
import json

from helpers import *

REST_SCHEMA = {
    'authenticate': '/auth/login',
    'get_user_info': '/auth',
    'logout': '/auth/logout',
    'status': '/status',
    'list_templates': '/list/templates/',
    'create_lab': '/labs',
    'delete_lab': '/labs/{lab_name}',
    'create_node': '/labs/{lab_name}/nodes',
    'get_node': '/labs/{lab_name}/nodes',
    'delete_node': '/labs/{lab_name}/nodes/{node_id}',
    'get_all_nodes': '/labs/{lab_name}/nodes',
    'get_node_interfaces': '/labs/{lab_name}/nodes/{node_id}/interfaces',
    'start_all_nodes': '/labs/{lab_name}/nodes/start',
    'stop_all_nodes': '/labs/{lab_name}/nodes/stop',
    'connect_interfaces': '/labs/{lab_name}/nodes/{node_id}/interfaces'
}


class UnetLab(RestServer):

    def __init__(self, address):
        super(UnetLab, self).__init__(address)

    def authenticate(self, user, pwd):
        api_call = REST_SCHEMA['authenticate']
        payload = {
            "username": user,
            "password": pwd
        }
        resp = self.add_object(api_call, data=payload)
        self.set_cookies(resp.cookies)
        return resp

    def get_user_info(self):
        api_call = REST_SCHEMA['get_user_info']
        resp = self.get_object(api_call)
        return resp

    def logout(self):
        api_call = REST_SCHEMA['logout']
        resp = self.get_object(api_call)
        return resp

    def get_status(self):
        api_call = REST_SCHEMA['status']
        resp = self.get_object(api_call)
        return resp

    def get_templates(self):
        api_call = REST_SCHEMA['list_templates']
        resp = self.get_object(api_call)
        return resp

    def create_lab(self, name):
        lab = UnlLab(self, name)
        return lab

    def delete_lab(self, name):
        api_call = REST_SCHEMA['delete_lab']
        api_url = api_call.format(api_call, lab_name=append_unl(name))
        resp = self.del_object(api_url)
        return resp


class UnlLab(object):

    def __init__(self, unl, name):
        api_call = REST_SCHEMA['create_lab']
        payload = {
           "path": "/",
           "name": name,
           "version": "1"
        }
        self.name = name
        self.unl = unl
        self.resp = self.unl.add_object(api_call, data=payload)

    def create_node(self, device):
        node = UnlNode(self, device)
        return node

    def delete_node(self, device):
        node_id = self.get_node_id_by_name(device.name)
        api_call = REST_SCHEMA['delete_node']
        api_url = api_call.format(api_call, lab_name=append_unl(self.name), node_id=node_id)
        resp = self.unl.del_object(api_url)
        return resp

    def get_nodes(self):
        api_call = REST_SCHEMA['get_all_nodes']
        api_url = api_call.format(api_call, lab_name=append_unl(self.name))
        resp = self.unl.get_object(api_url)
        return resp

    def get_node_id_by_name(self, node_name):
        node_dict = json.loads(self.get_nodes().content)['data']
        for node_id in node_dict:
            if node_dict[node_id]["name"] == node_name:
                return node_id
        return None

    def del_all_nodes(self):
        node_dict = json.loads(self.get_nodes().content)['data']
        for node_id in node_dict:
            self.delete_node(node_id)
        return None

    def start_all_nodes(self):
        api_call = REST_SCHEMA['start_all_nodes']
        api_url = api_call.format(api_call, lab_name=append_unl(self.name))
        resp = self.unl.get_object(api_url)
        return resp

    def stop_all_nodes(self):
        api_call = REST_SCHEMA['stop_all_nodes']
        api_url = api_call.format(api_call, lab_name=append_unl(self.name))
        resp = self.unl.get_object(api_url)
        return resp


class UnlNode(object):

    def __init__(self, lab, device):
        self.unl = lab.unl
        self.lab = lab
        self.device = device
        api_call = REST_SCHEMA['create_node']
        api_url = api_call.format(api_call, lab_name=append_unl(self.lab.name))
        payload = self.device.to_json()
        self.resp = self.unl.add_object(api_url, data=payload)

    def get_interfaces(self, node_id):
        api_call = REST_SCHEMA['get_node_interfaces']
        api_url = api_call.format(api_call, lab_name=append_unl(self.lab.name), node_id=node_id)
        resp = self.unl.get_object(api_url)
        return resp

    def get_node_id(self):
        return self.lab.get_node_id_by_name(self.device.name)

    def connect_interface(self, net_id):
        api_call = REST_SCHEMA['connect_interfaces']
        api_url = api_call.format(api_call, lab_name=append_unl(self.lab.name), node_id=self.get_node_id())
        payload = {self.device.get_next_interface() : net_id}
        resp = self.unl.update_object(api_url, data=payload)
        return resp

    def connect_node(self, other):
        self.add_net(name=net_name)
        net_id = self.get_net_by_name(net_name)
        node1_id = self.get_node_by_name(node1)
        node2_id = self.get_node_by_name(node2)
        resp1 = self.connect_interface(node1_id, net_id)
        resp2 = self.connect_interface(node2_id, net_id)
        return resp1, resp2


class UnlNet(object):

    def add_net(self, type='bridge', name = 'NET'):
        api_call = '/labs/{lab_name}/networks'
        payload = dict()
        payload['type'] = type
        payload['name'] = name
        api_url = api_call.format(api_call, lab_name=append_unl(LAB_NAME))
        resp = self.unl.add_object(api_url, data=payload)
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


def main():
    pass


if __name__ == '__main__':
    main()

