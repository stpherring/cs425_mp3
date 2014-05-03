import socket
import sys
from thread import *
import globes
from commands import *
from utils import *



def process_input(command):
    try:
        success = execute(command)
        if not success:
            print "Invalid command"
    except IndexError:
        print "Invalid command"



def execute(command):
    """ Execute a command either from the command prompt or from a message
        Returns True if the command is valid, else False. """
    params = command.split(" ")
    action = params[0]
    key = params[1]

    if action == "get" and len(params) == 3:
        level = int(params[2])
        get(key, level)

    elif action == "insert" and len(params) == 4:
        value = params[2]
        level = int(params[3])
        insert(key, value, level)

    elif action == "update" and len(params) == 4:
        value = params[2]
        level = int(params[3])
        update(key, value, level)

    elif action == "delete" and len(params) == 2:
        delete(key)

    else:
        return False

    return True



def recv_thread(args):
    """ Thread that receives and executes new messages """
    while True:
        message, addr = globes.sock.recvfrom(4096)
        success = execute(message)
        if not success:
            print "Error in recv: " + action + " not a valid action"



def main(argv):
    """ Get command line args """
    if len(argv) == 1:
        server_num = int(argv[0]);
        globes.init(server_num)
    else:
        print "Usage: python2 mp3.py <server # [0-3]>"
        sys.exit(2)

    try:
        globes.sock.bind( parse_addr( globes.get_my_address() ) )
    except socket.error, msg:
        print "Bind failed. Error Code: " + str(msg[0]) + " Message: " + msg[1]
        sys.exit()

    start_new_thread( recv_thread, ("no args",) )

    print "***** Enter a command *****"
    while True:
        command = raw_input(">>>")
        process_input(command)



if __name__ == "__main__":
    main(sys.argv[1:])
