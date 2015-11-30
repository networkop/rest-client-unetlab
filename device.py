
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

    def get_next_interface(self):
        for i in range():
            for index in Router.intf_list:
                yield index+i


class Switch(Device):
    def __init__(self, name):
        super(Router, self).__init__(name)


def main():
    d = Router('R1')
    print(d)
    print (d._to_json())

if __name__ == '__main__':
    main()