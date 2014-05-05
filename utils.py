""" Assorted utility functions for mp3 """

import socket
import globes
import random
from time import time, sleep


def parse_addr(address):
    """ Given an address like localhost:15000, return a pair (host_ip, port) """
    ip_components = address.split(':')
    host = ip_components[0]
    port = int(ip_components[1])
    try:
        host_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print 'Hostname could not be resolved. Exiting.'
        sys.exit()
    return (host_ip, port)



def random_delay(dest_server_num):
    """ Sleep for a random amount of time, based on the config file.
        Multiply by 2 to make average delay time - linearity of expectation """
    avg_delay = globes.get_avg_delay( dest_server_num )
    delay = random.uniform(0, 2 * avg_delay)
    sleep(delay)



def send_command(dest_server_num, command, time, command_counter):
    """ Send a command to a server with the specified server numer 
        Commands are of the form """
    random_delay( dest_server_num )
    addr = globes.get_command_address( dest_server_num )
    message = str(command_counter) + "#" + command + "#" + str(time)
    globes.command_sock.sendto( message, addr )



def send_reply(reply, counter, time, dest_addr):
    """ Send a reply message to dest_addr. dest_addr is a tuple of the form (ip, port) """
    dest_server_num = match_addr_to_server_num(dest_addr)
    random_delay( dest_server_num )
    addr = globes.get_reply_address( dest_server_num )
    message = str(counter) + "#" + reply + "#" + str(time)
    globes.reply_sock.sendto( message, addr )



def create_timestamp():
    """ Get the current time (in floating point seconds) to be preprended to every message """
    return time()



def hash(key):
    """ The hash function used to map a key to a server in the chord """
    return key % globes.total_servers



def all_replica_nums(key):
    """ Return a list of all the server_nums that contain a replica of this key """
    key = int(key)
    return [ hash(key-1), hash(key), hash(key+1) ]


def all_server_nums():
    """ Return a list of all the server_nums, with no regard to a key or hash """
    return [i for i in range(globes.total_servers)]


def match_addr_to_server_num(addr):
    """ Given an address tuple, return the server_num that has that socket """
    target_port = addr[1]
    offset = globes.port_offset
    for i in range(len(globes.addresses)):
        curr_port = int(globes.addresses[i].split(":")[1])
        if curr_port == target_port or curr_port == target_port-offset or curr_port == target_port+offset:
            return i



def get_timestamp(value):
    return value.split('#')[2]


def get_counter(value):
    return int(value.split('#')[0])

def get_command(value):
    return value.split('#')[1]
