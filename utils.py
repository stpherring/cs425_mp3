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



def send_command(dest_server_num, command, time):
    """ Send a command to a server with the specified server numer 
        Commands are of the form """
    random_delay( dest_server_num )
    addr = globes.get_command_address( dest_server_num )
    message = str(globes.command_counter) + "#" + command + "#" + str(time)
    globes.command_sock.sendto( message, addr )



def send_reply(reply, time, src_addr):
    """ Send a reply to a server with the specified server numer
        src_addr is the address of the socket who sent the command """
    dest_server_num = match_addr_to_server_num(src_addr)
    random_delay( dest_server_num )
    addr = globes.get_reply_address( dest_server_num )
    message = str(time) + "#" + reply
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



def match_addr_to_server_num(addr):
    """ Given an address tuple, return the server_num that has that socket """
    for i in range(len(globes.addresses)):
        if int(globes.addresses[i].split(":")[1]) == addr[1]: # if port number matches
            return i



def get_timestamp(value):
    return value.split('#')[2]


def get_counter(value):
    print """ERROR Stephen, your reply messages do not have a counter in them.
        See here, you call get_counter() with parameter """, value
    return int(value.split('#')[0])


