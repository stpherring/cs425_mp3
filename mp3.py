import socket
import sys
from thread import *
import globes
from utils import *



def process_input(command, time):
    try:
        success = execute(command, time)
        if not success:
            print "Invalid command"
    except IndexError:
        print "Invalid command"



def execute(command, time):
    """ Execute a command either from the command prompt or from a message
        Returns True if the command is valid, else False. """
    params = command.split(" ")
    action = params[0]
    key = params[1]

    print "key {0} hashes to {1}".format(key, hash(int(key)))

    if action == "get" and len(params) == 3:
        level = int(params[2])
        globes.db.get(key, level)

    elif action == "insert" and len(params) == 4:
        value = params[2]
        level = int(params[3])
        globes.db.insert(key, value, level)

    elif action == "update" and len(params) == 4:
        value = params[2]
        level = int(params[3])
        globes.db.update(key, value, level)

    elif action == "delete" and len(params) == 2:
        globes.db.delete(key)

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
        time = create_timestamp()
        process_input(command, time)



if __name__ == "__main__":
    main(sys.argv[1:])
