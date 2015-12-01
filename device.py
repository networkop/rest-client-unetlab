
class Device(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "This is device " + self.name

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

    def get_next_interface(self):
        result = self.offset + Router.intf_list[self.index]
        self.offset += 1
        self.index += 1
        if self.index > 3:
            self.index = 0
            self.offset += 1
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