import socket
import sys
from thread import *
import globes
from utils import *
from command_parser import *



def process_input(command, time):
    """ Execute a command either from the command prompt or from a message
        Returns True if the command is valid, else False. """
    if is_valid_command(command):
        coordinate_command(command, time)
    else:
        print "Invalid command"



def coordinate_command(command, time):
    """ Coordinate a get call. Send request to all replicas and wait for one or all responses """
    replicas = all_replica_nums( get_key(command) )
    for replica_num in replicas:
        send_command(replica_num, command, time) # send to all replicas
    
    if is_get(command):
        # wait to receive the value from one or all replicas
        print "waiting for get values"
        value, addr = globes.reply_sock.recvfrom(4096)
        print "received get value " + value
    elif is_insert(command):
        # wait to receive success message from one or all replicas
        print "waiting for insert success"
    elif is_update(command):
        # wait to receive success message from one or all replicas
        print "waiting for update success"

    # delete does not require waiting. it has no consistency level.



def execute(command, timestamp, src_addr):
    """ Execute a command either from the command prompt or from a message.
        This actually does the execution on this server -- not message passing and waiting """

    if is_get(command):
        print "executing get on this machine"
        send_reply("value", timestamp, src_addr)

    elif is_insert(command):
        print "executing insert on this machine"
        send_reply("successfully inserted", timestamp, src_addr)

    elif is_update(command):
        print "executing update on this machine"
        send_reply("successfully updated", timestamp, src_addr)

    elif is_delete(command):
        print "executing delete on this machine"

    else:
        return False

    return True



def recv_thread(args):
    """ Thread that receives and executes new messages """
    while True:
        message, addr = globes.command_sock.recvfrom(4096)
        [timestamp, command] = message.split("#")
        success = execute(command, timestamp, addr)
        if not success:
            print "Error in recv: " + command + " not a valid command"



def main(argv):
    """ Get command line args """
    if len(argv) == 1:
        server_num = int(argv[0]);
        globes.init(server_num)
    else:
        print "Usage: python2 mp3.py <server # [0-3]>"
        sys.exit(2)

    try:
        globes.command_sock.bind( globes.get_my_command_address() )
        globes.reply_sock.bind( globes.get_my_reply_address() )
    except socket.error, msg:
        print "Bind failed. Error Code: " + str(msg[0]) + " Message: " + msg[1]
        sys.exit()

    start_new_thread( recv_thread, ("no args",) )

    print "***** Enter a command *****"
    while True:
        command = raw_input(">>>")
        time = create_timestamp()
        process_input(command, time)



if __name__ == "__main__":
    main(sys.argv[1:])

