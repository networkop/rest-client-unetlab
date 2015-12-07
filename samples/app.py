from restunl.helpers import *
from restunl.unetlab import UnetLab
from restunl.device import Router

LAB_NAME = 'test_1'


def cleanup(unl, lab):
    lab.stop_all_nodes()
    lab.del_all_nodes()
    unl.delete_lab(LAB_NAME)
    return None


def main():
    unl = UnetLab('192.168.247.20')
    unl.authenticate('admin', 'unl')
    unl.delete_lab(LAB_NAME)
    lab = unl.create_lab(LAB_NAME)
    lab.stop_all_nodes()
    try:
        node_1 = lab.create_node(Router('R1'))
        print "node 1 created"
        node_2 = lab.create_node(Router('R2'))
        node_1.connect_node(node_2)
        lab.start_all_nodes()
        print "nodes started"
        conf_1 = read_file('.\\configs\\R1.txt')
        conf_2 = read_file('.\\configs\\R2.txt')
        node_1.configure(conf_1)
        print "node 1 configured"
        node_2.configure(conf_2)
    except:
        cleanup(unl, lab)
    #cleanup(cleanup(unl, lab))


if __name__ == '__main__':
    main()
