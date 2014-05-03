""" Define the global variables for mp3.py """

import socket
import json


def init(num):
    """ Initialization function. Must be explicitly called: globes.init(n) """

    global server_num
    global delays
    global addresses
    global sock

    server_num = num

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # read in the config.json file to initialize delays and addresses
    config_json = open('config.json')
    data = json.load(config_json)
    delays = data['avg_delays'][server_num] # delays is a list of avg delay times
    addresses = data['addresses']


def get_address(server_num):
    """ Getter returns the address of server_num """
    return addresses[server_num]


def get_my_address():
    """ Called by server_num.  Returns addresses[server_num] """
    return addresses[server_num]


def get_avg_delay(dest_server_num):
    """ Getter returns the average delay time for a send to server_num """
    return delays[server_num]