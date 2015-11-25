import requests
import json
import device
from helpers import *

UNETLAB_ADDRESS = '192.168.247.20'
USERNAME = "admin"
PASSWORD = "unl"
LAB_NAME = 'test_rest'


class UnetLab(object):
    rest_object = 'api'

    def __init__(self):
        self.cookies = None
        self.base_url = '/'.join(['http:/', UNETLAB_ADDRESS, self.rest_object])

    def _send_request(self, method, path, data=None):
        response = None
        url = self.base_url + path
        try:
            response = requests.request(method, url,  json=data,
                                        cookies=self.cookies)
        except requests.exceptions.RequestException as e:
            print('Error calling %s: %s', url, e.message)
        return response

    def _get_object(self, api_call, data=None):
        resp = self._send_request('GET', api_call, data)
        return resp

    def _add_object(self, api_call, data=None):
        resp = self._send_request('POST', api_call, data)
        return resp

    def _del_object(self, api_call, data=None):
        resp = self._send_request('DELETE', api_call, data)
        return resp

    def authenticate(self, user, pwd):
        api_call = '/auth/login'
        api_method = 'POST'
        payload = {
            "username": user,
            "password": pwd
        }
        resp = self._send_request(api_method, api_call,
                                  data=payload)
        self.cookies = resp.cookies
        return resp

    def get_user_info(self):
        api_call = '/auth'
        resp = self._get_object(api_call)
        return resp

    def logout(self):
        api_call = '/auth/logout'
        resp = self._get_object(api_call)
        return resp

    def get_status(self):
        api_call = '/status'
        resp = self._get_object(api_call)
        return resp

    def get_templates(self):
        api_call = '/list/templates'
        resp = self._get_object(api_call)
        return resp


class UnlLabs(UnetLab):

    def create_lab(self, name=LAB_NAME):
        api_call = '/labs'
        payload = {
           "path": "/",
           "name": name,
           "version": "1"
        }
        resp = self._add_object(api_call, data=payload)
        return resp

    def delete_lab(self, name=LAB_NAME):
        api_call = '/labs/{lab_name}'
        api_url = api_call.format(api_call, lab_name=append_unl(name))
        resp = self._del_object(api_url)
        return resp

    def add_node(self, dev):
        api_call = '/labs/{lab_name}/nodes'
        api_url = api_call.format(api_call, lab_name=append_unl(LAB_NAME))
        payload = dev.to_json()
        resp = self._add_object(api_url, data=payload)
        return resp

    def get_nodes(self):
        api_call = '/labs/{lab_name}/nodes'
        api_url = api_call.format(api_call, lab_name=append_unl(LAB_NAME))
        resp = self._get_object(api_url)
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
        resp = self._get_object(api_url)
        return resp

    def del_node(self, node_id):
        api_call = '/labs/{lab_name}/nodes/{node_id}'
        api_url = api_call.format(api_call, lab_name =append_unl(LAB_NAME), node_id=node_id)
        resp = self._del_object(api_url)
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
        resp = self._add_object(api_url, data=payload)
        return resp
     
    def get_nets(self):
        api_call = '/labs/{lab_name}/networks'
        api_url = api_call.format(api_call, lab_name=append_unl(LAB_NAME))
        resp = self._get_object(api_url)
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
        resp = self._del_object(api_url)
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
        resp = self._send_request(api_method, api_url, data=payload)
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
        api_url = api_call.format(api_call, lab_name = append_unl(LAB_NAME))
        resp = self._get_object(api_url)
        return resp


def main():
    unl = UnetLab()
    unl.authenticate(USERNAME, PASSWORD)
    #print unl.is_authenticated()
    unl.delete_lab(LAB_NAME)
    unl.create_lab(LAB_NAME)
    #unl.delete_lab(LAB_NAME)
    r1 = device.Router('R1')
    r2 = device.Router('R2')
    unl.add_node(r1)
    unl.add_node(r2)
    #unl.add_net()
    unl.connect_nodes("R1", "R2")
    unl.start_all_nodes()
    #unl.del_all_nodes()
    #unl.del_all_nets()
    unl.get_nodes()
    unl.get_nets()

if __name__ == '__main__':
    main()

