from utils import *
from command_parser import *

def search(key):
    """ This should not be a separate file. It is right now to avoid merging """
    """ Send a get request to all replicas. Do not do read repair. """

    ## just copy paste get all
    ## wait for all responses and then print out all the keys
    ## but do NOT do read repair
    for replica_num in replicas:
        start_new_thread( send_command, (replica_num, command, timestamp, globes.command_counter) ) # send to all replicas
    globes.command_counter += 1

    while num_replies < globes.num_replicas:
        content, addr = globes.reply_sock.recvfrom(4096)
        received_counter = get_counter(content)
        if received_counter == c_counter:
            received_timestamp = float(get_timestamp(content))
            reply = get_command(content)
            print "Received " + reply + " from " + addr
            num_replies += 1
        else:
            send_reply(get_command(content), get_counter(content), get_timestamp(content), globes.get_my_reply_address() )
