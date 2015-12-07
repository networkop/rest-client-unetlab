from restunl.client import RestServer
from restunl.helpers import *
import json

REST_SCHEMA = {
    'authenticate': '/auth/login',
    'get_user_info': '/auth',
    'logout': '/auth/logout',
    'status': '/status',
    'add_user': '/users',
    'list_templates': '/list/templates/',
    'create_lab': '/labs',
    'delete_lab': '/labs/{lab_name}',
    'create_node': '/labs/{lab_name}/nodes',
    'create_net': '/labs/{lab_name}/networks',
    'get_node': '/labs/{lab_name}/nodes/{node_id}',
    'delete_node': '/labs/{lab_name}/nodes/{node_id}',
    'delete_net': '/labs/{lab_name}/networks/{net_id}',
    'get_all_nodes': '/labs/{lab_name}/nodes',
    'get_all_nets': '/labs/{lab_name}/networks',
    'get_node_interfaces': '/labs/{lab_name}/nodes/{node_id}/interfaces',
    'start_all_nodes': '/labs/{lab_name}/nodes/start',
    'stop_all_nodes': '/labs/{lab_name}/nodes/stop',
    'connect_interfaces': '/labs/{lab_name}/nodes/{node_id}/interfaces'
}


class UnetLab(RestServer):

    def __init__(self, address):
        super(UnetLab, self).__init__(address)

    def authenticate(self, user, pwd):
        self.set_creds(user, pwd)
        return self._do_authenticate(user, pwd)

    def _do_authenticate(self, user, pwd):
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

    def add_user(self, name, pwd, role):
        api_call = REST_SCHEMA['add_user']
        payload = {
            'username': name,
            'name': name,
            'password': pwd,
            'email': 'test@unl.com',
            'role': role
        }
        resp = self.add_object(api_call, data=payload)
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

    def create_net(self, name):
        net = UnlNet(self, name)
        return net

    def delete_net(self, net_id):
        api_call = REST_SCHEMA['delete_net']
        api_url = api_call.format(api_call, lab_name=append_unl(self.name), net_id=net_id)
        resp = self.unl.del_object(api_url)
        return resp

    def create_node(self, device):
        node = UnlNode(self, device)
        return node

    def delete_node(self, node_id):
        api_call = REST_SCHEMA['delete_node']
        api_url = api_call.format(api_call, lab_name=append_unl(self.name), node_id=node_id)
        resp = self.unl.del_object(api_url)
        return resp

    def get_nodes(self):
        api_call = REST_SCHEMA['get_all_nodes']
        api_url = api_call.format(api_call, lab_name=append_unl(self.name))
        resp = self.unl.get_object(api_url)
        return resp

    def get_nets(self):
        api_call = REST_SCHEMA['get_all_nets']
        api_url = api_call.format(api_call, lab_name=append_unl(self.name))
        resp = self.unl.get_object(api_url)
        return resp

    def get_node_id_by_name(self, node_name):
        node_dict = json.loads(self.get_nodes().content)['data']
        return get_id_by_name(node_dict, node_name)

    def get_net_id_by_name(self, net_name):
        net_dict = json.loads(self.get_nets().content)['data']
        return get_id_by_name(net_dict, net_name)

    def del_all_nodes(self):
        node_dict = json.loads(self.get_nodes().content)['data']
        for node_id in node_dict:
            self.delete_node(node_id)
        return None

    def del_all_nets(self):
        nets_dict = json.loads(self.get_nets().content)['data']
        for node_id in nets_dict:
            self.delete_net(node_id)
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

    def cleanup(self):
        self.stop_all_nodes()
        self.del_all_nodes()
        return None


class UnlNode(object):

    def __init__(self, lab, device):
        self.unl = lab.unl
        self.lab = lab
        self.device = device
        api_call = REST_SCHEMA['create_node']
        api_url = api_call.format(api_call, lab_name=append_unl(self.lab.name))
        payload = self.device.to_json()
        self.resp = self.unl.add_object(api_url, data=payload)

    def get_interfaces(self):
        api_call = REST_SCHEMA['get_node_interfaces']
        api_url = api_call.format(api_call, lab_name=append_unl(self.lab.name), node_id=self.get_node_id())
        resp = self.unl.get_object(api_url)
        return resp

    def get_node_id(self):
        return self.lab.get_node_id_by_name(self.device.name)

    def get_config(self):
        api_call = REST_SCHEMA['get_node']
        api_url = api_call.format(api_call, lab_name=append_unl(self.lab.name), node_id=self.get_node_id())
        resp = self.unl.get_object(api_url)
        return resp

    def connect_interface(self, net):
        api_call = REST_SCHEMA['connect_interfaces']
        api_url = api_call.format(api_call, lab_name=append_unl(self.lab.name), node_id=self.get_node_id())
        payload = {str(self.device.get_next_interface()): net.get_net_id()}
        resp = self.unl.update_object(api_url, data=payload)
        return resp

    def connect_node(self, other):
        net = self.lab.create_net(name='_'.join([self.device.name, other.device.name]))
        resp1 = self.connect_interface(net)
        resp2 = other.connect_interface(net)
        return resp1, resp2

    def get_url(self):
        return json.loads(self.get_config().content)['data']['url']

    def configure(self, conf):
        self.device.set_url(self.get_url())
        return self.device.set_config(conf)


class UnlNet(object):

    def __init__(self, lab, name):
        api_call = REST_SCHEMA['create_net']
        self.unl = lab.unl
        self.lab = lab
        self.name = name
        payload = dict()
        payload['type'] = 'bridge'
        payload['name'] = self.name
        api_url = api_call.format(api_call, lab_name=append_unl(self.lab.name))
        self.resp = self.unl.add_object(api_url, data=payload)

    def get_net_id(self):
        return self.lab.get_net_id_by_name(self.name)


def main():
    pass

if __name__ == '__main__':
    main()

