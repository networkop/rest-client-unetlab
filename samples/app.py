from restunl.helpers import *
from restunl.unetlab import UnetLab
from restunl.device import Router

LAB_NAME = 'test_1'


def app_1():
    unl = UnetLab('192.168.247.20')
    unl.authenticate('admin', 'unl')
    print ("*** CONNECTED TO UNL")
    lab = unl.create_lab(LAB_NAME)
    lab.cleanup()
    try:
        node_1 = lab.create_node(Router('R1'))
        print ("*** NODE 1 STARTED")
        node_2 = lab.create_node(Router('R2'))
        print ("*** NODE 2 STARTED")
        node_1.connect_node(node_2)
        lab.start_all_nodes()
        print ("*** ALL NODES STARTED")
        conf_1 = read_file('.\\configs\\R1.txt')
        conf_2 = read_file('.\\configs\\R2.txt')
        node_1.configure(conf_1)
        print ("*** CONFIG PUSHED TO NODE 1")
        node_2.configure(conf_2)
        print ("*** CONFIG PUSHED TO NODE 2")
        raw_input('PRESS ANY KEY TO STOP THE LAB')
        raw_input('*** CLEANING UP THE LAB')
        lab.cleanup()
    except Exception as e:
        print ("*** SOMETHING FAILED ")
        lab.cleanup()
        raise e
    finally:
        unl.delete_lab(LAB_NAME)

if __name__ == '__main__':
    app_1()
