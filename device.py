import telnetlib
import time
from helpers import *


class Device(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return type(self).__name__ + '(' + self.name + ')'

    def to_json(self):
        return self.__dict__


class Router(Device):
    defaults = {
        'template': 'iol',
        'count': 1,
        'image': 'L3-ADVENTERPRISEK9-M-15.4-1T.bin',
        'ram': '256',
        'ethernet': '2',
        'serial': '0',
        'type': 'iol',
        'config': 'unconfigured'
    }
    intf_list = [0, 16, 32, 48]

    def __init__(self, name):
        for key, value in Router.defaults.items():
            setattr(self, key, value)
        super(Router, self).__init__(name)
        self.offset = 0
        self.index = 0
        self.url_ip, self.url_port = '', ''

    def get_next_interface(self):
        result = self.offset + Router.intf_list[self.index]
        self.offset += 1
        self.index += 1
        if self.index > 3:
            self.index = 0
            self.offset += 1
        return result

    def set_url(self, url):
        self.url_ip, self.url_port = str(url).strip('telnet://').split(':')
        return None

    def __wait_vty(self, session, stop_char='>'):
        result = ' ' + session.read_very_eager()
        while stop_char not in result[-10:]:
            session.write('\n')
            result += session.read_very_eager()
            time.sleep(0.1)
        return result

    def set_config(self, config):
        session = telnetlib.Telnet(self.url_ip, self.url_port)
        temp = self.__wait_vty(session, stop_char='#')
        print 'BEFORE CONFIG \n' + temp
        t = wrap_command(config)
        session.write(t)
        temp = self.__wait_vty(session, stop_char='#')
        print 'AFTER CONFIG \n' + temp
        session.close()
        return None

    def verify_config(self, text):
        session = telnetlib.Telnet(self.url_ip, self.url_port)
        temp = self.__wait_vty(session)
        print 'BEFORE VERIFY \n' + temp
        session.write(wrap_command(text))
        result = self.__wait_vty(session, stop_char='#')
        print "VERIFYING \n" + result
        session.close()
        return result


class Switch(Device):
    def __init__(self, name):
        super(Router, self).__init__(name)


def main():
    d = Router('R1')
    print(d)
    print (d._to_json())

if __name__ == '__main__':
    main()