import requests

BASE_URL = 'api'


class RestServer(object):

    def __init__(self, address):
        self.cookies = None
        self.base_url = '/'.join(['http:/', address, BASE_URL])

    def _send_request(self, method, path, data=None):
        response = None
        url = self.base_url + path
        try:
            response = requests.request(method, url,  json=data, cookies=self.cookies)
        except requests.exceptions.RequestException as e:
            print('Error calling %s: %s', url, e.message)
        return response

    def set_cookies(self, cookie):
        self.cookies = cookie

    def get_object(self, api_call, data=None):
        resp = self._send_request('GET', api_call, data)
        return resp

    def add_object(self, api_call, data=None):
        resp = self._send_request('POST', api_call, data)
        return resp

    def del_object(self, api_call, data=None):
        resp = self._send_request('DELETE', api_call, data)
        return resp


def main():
    pass

if __name__ == '__main__':
    main()

