import requests
import json
from requests.auth import HTTPBasicAuth

UNETLAB_ADDRESS = '192.168.247.10'
USERNAME = "admin"
PASSWORD = "unl"
BASE_URL = '/api'
LAB_NAME = 'test_rest'
IOL_L3_IMAGE = 'L3-ADVENTERPRISEK9-M-15.4-1T.bin'

class UnetLab():
    def __init__(self):
        self.cookies = None
        self.base_url = 'http://' + UNETLAB_ADDRESS + BASE_URL

    def _do_request(self, method, path, params=None, data=None):
        response = None
        url = self.base_url + path
        headers = {'Content-type': 'application/json'}
        # send data as string
        data = json.dumps(data)
        try:
            response = requests.request(method, url, headers=headers, data=data, cookies=self.cookies)
        except requests.exceptions.RequestException as e:
            print('Error while calling %s: %s', url, e.message)
        return response

    def _append_unl(self, name): 
        return name + ".unl"

    def _construct(self, device_type, name):
        data = {}
        data['template'] = 'iol'
        data['count'] = '1'
        data['image'] = IOL_L3_IMAGE
        data['name'] = name
        data['ram'] = "256"
        data['ethernet'] = "1" 
        data['serial'] = "0"
        data['type'] = "iol"
        data['config'] = "unconfigured"
        return data

    def authenticate(self, user, pwd):
        api_call = '/auth/login'
        api_method = 'POST'
        payload = { "username": user, "password": pwd }
        resp = self._do_request(api_method, api_call, data=payload)
        self.cookies = resp.cookies
        return resp.json()

    def is_authenticated(self):
        api_call = '/auth'
        api_method = 'GET'
        resp = self._do_request(api_method, api_call)
        return resp.content

    def create_lab(self, name):
        api_call = '/labs'
        api_method = 'POST'
        payload = {
           "path": "/",
           "name": name,
           "version": "1"
        }
        resp = self._do_request(api_method, api_call, data=payload)
        print resp.content
        return resp.content

    def delete_lab(self, name):
        api_call = '/labs/{lab_name}'
        api_method = 'DELETE'
        api_url = api_call.format(api_call, lab_name = self._append_unl(name))
        resp = self._do_request(api_method, api_url)
        print resp.content
        return resp.content

    def add_node(self, device, name):
        api_call = '/labs/{lab_name}/nodes'
        api_method = 'POST'
        api_url = api_call.format(api_call, lab_name = self._append_unl(LAB_NAME))
        payload = self._construct(device, name)
        print payload
        resp = self._do_request(api_method, api_url, data=payload)
        print resp.content
        return resp.content

    def get_nodes(self):
        api_call = '/labs/{lab_name}/nodes'
        api_method = 'GET'
        api_url = api_call.format(api_call, lab_name = self._append_unl(LAB_NAME))
        resp = self._do_request(api_method, api_url)
        print resp.content
        return resp.content
  
    def get_node_by_name(self, node_name):
        node_dict = json.loads(self.get_nodes())['data']
        for node_id in node_dict:
            if node_dict[node_id]["name"] == node_name:
               return node_id
        return None 
  
    def get_node_interfaces(self, node_id):
        api_call = '/labs/{lab_name}/nodes/{node_id}/interfaces'
        api_method = 'GET'
        api_url = api_call.format(api_call, lab_name = self._append_unl(LAB_NAME), node_id = node_id)
        print "url = " + str(api_url)
        resp = self._do_request(api_method, api_url)
        print "interface list " + str(resp)
        return resp

    def del_node(self, node_id):
        api_call = '/labs/{lab_name}/nodes/{node_id}'
        api_method = 'DELETE'
        api_url = api_call.format(api_call, lab_name = self._append_unl(LAB_NAME), node_id = node_id)
        resp = self._do_request(api_method, api_url)
        print resp.content
        return resp.content

    def del_all_nodes(self):
        node_dict = json.loads(self.get_nodes())['data']
        for node_id in node_dict:
            self.del_node(node_id)
        return

    def add_net(self, type='bridge', name = 'NET'):
        api_call = '/labs/{lab_name}/networks'
        api_method = 'POST'
        payload = {}
        payload['type'] = type
        payload['name'] = name
        api_url = api_call.format(api_call, lab_name = self._append_unl(LAB_NAME))
        resp = self._do_request(api_method, api_url, data=payload)
        print resp.content
        return resp.content
     
    def get_nets(self):
        api_call = '/labs/{lab_name}/networks'
        api_method = 'GET'
        api_url = api_call.format(api_call, lab_name = self._append_unl(LAB_NAME))
        resp = self._do_request(api_method, api_url)
        print resp.content
        return resp.content
 
    def get_net_by_name(self, net_name):
        nets_dict = json.loads(self.get_nets())['data']
        for net_id in nets_dict:
            if nets_dict[net_id]["name"] == net_name:
                return net_id
        return None

    def del_net(self, net_id):
        api_call = '/labs/{lab_name}/networks/{net_id}'
        api_method = 'DELETE'
        api_url = api_call.format(api_call, lab_name = self._append_unl(LAB_NAME), net_id = net_id)
        resp = self._do_request(api_method, api_url)
        print resp.content
        return resp.content
  
    def del_all_nets(self):
        nets_dict = json.loads(self.get_nets())['data']
        for node_id in nets_dict:
            self.del_net(node_id)
        return

    def connect_interface(self, node_id, net_id):
        api_call = '/labs/{lab_name}/nodes/{node_id}/interfaces'
        api_method = 'PUT'
        api_url = api_call.format(api_call, lab_name = self._append_unl(LAB_NAME), node_id = node_id)
        payload = {"0": net_id} 
        print self.get_node_interfaces(node_id)
        resp = self._do_request(api_method, api_url, data=payload)
        print resp.content
        return resp.content

    def connect_nodes(self, node1, node2):
        net_name = "ONE"
        self.add_net(name=net_name)
        net_id = self.get_net_by_name(net_name)
        node1_id = self.get_node_by_name(node1)
        node2_id = self.get_node_by_name(node2)
        self.connect_interface(node1_id, net_id)
        self.connect_interface(node2_id, net_id)

    def start_all_nodes(self):
        api_call = '/labs/{lab_name}/nodes/start'
        api_method = 'GET'
        api_url = api_call.format(api_call, lab_name = self._append_unl(LAB_NAME))
        resp = self._do_request(api_method, api_url)
        return resp.content
        
        

def main():
    unl = UnetLab()
    unl.authenticate(USERNAME, PASSWORD)
    print unl.is_authenticated()
    unl.delete_lab(LAB_NAME)
    unl.create_lab(LAB_NAME)
    #unl.delete_lab(LAB_NAME)
    unl.add_node('router','R1')
    unl.add_node('router','R2')
    #unl.add_net()
    unl.connect_nodes("R1","R2")
    unl.start_all_nodes()
    #unl.del_all_nodes()
    #unl.del_all_nets()
    unl.get_nodes()
    unl.get_nets()

if __name__ == '__main__':
    main()

