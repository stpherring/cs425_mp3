""" Define the global variables for mp3.py """

import socket
import json
from datastore import Datastore
from utils import parse_addr

port_offset = 100

def init(num):
    """ Initialization function. Must be explicitly called: globes.init(n) """

    global server_num       # this server's number (i.e. this instance)
    global total_servers    # the total number of servers in the system (usually 4)
    global command_sock     # this server's UDP socket for sending/receiving commands
    global reply_sock       # this server's UDP socket for receiving reply values/successes
    global db               # this server's Datastore object
    global delays           # delays[i] returns the avg delay from this server to server i
    global addresses        # addresses[i] returns the 'localhost:1500#' of server i
    global num_replicas     # number of replicas for each key
    global command_counter  # counter for the number of commands send

    server_num = num

    command_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    reply_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    db = Datastore()

    # read in the config.json file to initialize delays and addresses
    config_json = open('config.json')
    data = json.load(config_json)
    delays = data['avg_delays'][server_num] # delays is a list of avg delay times
    addresses = data['addresses']

    total_servers = len(addresses)

    num_replicase = 3


def get_command_address(server_num):
    """ Getter returns the address of server_num """
    return parse_addr( addresses[server_num] )


def get_my_command_address():
    """ Called by server_num.  Returns addresses[server_num] """
    return parse_addr( addresses[server_num] )


def get_reply_address(server_num):
    """ Getter returns the address of server_num """
    host_ip, port = parse_addr( addresses[server_num] )
    return host_ip, port + port_offset


def get_my_reply_address():
    """ Called by server_num.  Returns addresses[server_num] """
    host_ip, port = parse_addr( addresses[server_num] )
    return host_ip, port + port_offset


def get_avg_delay(dest_server_num):
    """ Getter returns the average delay time for a send to server_num """
    return delays[server_num]


