import requests

BASE_URL = 'api'


class RestServer(object):

    def __init__(self, address):
        self.cookies = None
        self.base_url = '/'.join(['http:/', address, BASE_URL])
        self.user, self.pwd = '', ''

    def set_creds(self, user, pwd):
        self.user = user
        self.pwd = pwd
        return None

    def _do_authenticate(self):
        raise NotImplementedError

    def _send_request(self, method, path, data=None):
        response = None
        url = self.base_url + path
        try:
            response = requests.request(method, url,  json=data, cookies=self.cookies)
        except requests.exceptions.RequestException as e:
            print('*** Error calling %s: %s', url, e.message)
        if self.cookies and 400 <= response.status_code <= 499:
            self._do_authenticate(self.user, self.pwd)
        return response

    def set_cookies(self, cookie):
        self.cookies = cookie

    def get_object(self, api_call, data=None):
        resp = self._send_request('GET', api_call, data)
        return resp

    def add_object(self, api_call, data=None):
        resp = self._send_request('POST', api_call, data)
        return resp

    def update_object(self, api_call, data=None):
        resp = self._send_request('PUT', api_call, data)
        return resp

    def del_object(self, api_call, data=None):
        resp = self._send_request('DELETE', api_call, data)
        return resp


def main():
    pass

if __name__ == '__main__':
    main()

