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

def get_remaining_replies(command, time, first_value, counter):
    """ This function gets the remaining replies from a command with ONE level consistency"""
    num_received = 0
    if is_get(command):
        latest_value = first_value
        latest_timestamp = get_timestamp(first_value)
        needsRepair = False
        # If command is "get" then we have to do inconsistency repair
        while num_received < globes.num_replicas - 1:
            value, addr = globes.reply_sock.recvfrom(4096)
            if counter == received_counter:
                num_received += 1
                received_timestamp = int(get_timestamp(value))
                if received_timestamp > latest_timestamp:
                    latest_timestamp = received_timestamp
                    latest_value = value
                    needsRepair = True
            else:
                # Send back to reply_sock (not sure how to do this)
        if needsRepair:
            print "Executing repair"
            replicas = all_replica_nums( command_parser.get_key(command) )
            for replica_num in replicas:
                rep_command = "insert " + command_parser.get_key(command) + " " command_parser.get_value(command)
                send_command(replica_num, , str(latest_timestamp))
            globes.command_counter += 1
    else:
        while num_received < globes.num_replicas - 1:
            value, addr = globes.reply_sock.recvfrom(4096)
            received_counter = get_counter(value)
            if counter == received_counter:
                num_received += 1
            else: 
                # Send back to reply_sock



def coordinate_command(command, time):
    """ Coordinate a get call. Send request to all replicas and wait for one or all responses """
    replicas = all_replica_nums( get_key(command) )
    for replica_num in replicas:
        send_command(replica_num, command, timestamp) # send to all replicas
    globes.command_counter += 1

    # GET
    if is_get(command):
        # wait to receive the value from one or all replicas
        print "waiting for get values"
        level = command_parser.get_level(command)
        if level == "1":
            num_replies = 0
            while num_replies < 1:
                value, addr = globes.reply_sock.recvfrom(4096)
                received_counter = get_counter(value)
                if received_counter == globes.command_counter:
                    num_replies += 1
                    counter = received_counter
                    start_new_thread(get_remaining_replies, (command, time, value, received_counter))
        if level == "9":
            num_replies = 0
            key_timestamp = 0
            while num_replies < globes.num_replicas:
                content, addr = globes.reply_sock.recvfrom(4096)
                received_counter, reply = split_reply(content)
                if received_counter == globes.command_counter:
                    num_replies += 1
        print "received get value " + reply
    
    # INSERT
    elif is_insert(command):
        # wait to receive success message from one or all replicas
        print "waiting for insert success"
        if level == "1":
            num_replies = 0
            while num_replies < 1:
                value, addr = globes.reply_sock.recvfrom(4096)
                received_counter = get_counter(value)
                if received_counter == globes.command_counter:
                    num_replies += 1
                    counter = received_counter
                    start_new_thread(get_remaining_replies, (command, time, value, received_counter))
        if level == "9":
            num_replies = 0
            key_timestamp = 0
            while num_replies < globes.num_replicas:
                content, addr = globes.reply_sock.recvfrom(4096)
                received_counter, reply = split_reply(content)


        print "insert successful"        

        
    # UPDATE
    elif is_update(command):
        # wait to receive success message from one or all replicas
        print "waiting for update success"

        if level == "1":
            num_replies = 0
            while num_replies < 1:
                value, addr = globes.reply_sock.recvfrom(4096)
                received_counter = get_counter(value)
                if received_counter == globes.command_counter:
                    num_replies += 1
                    counter = received_counter
                    start_new_thread(get_remaining_replies, (command, time, value, received_counter))
        if level == "9":
            num_replies = 0
            key_timestamp = 0
            while num_replies < globes.num_replicas:
                content, addr = globes.reply_sock.recvfrom(4096)
                received_counter, reply = split_reply(content)

        print "update successful"

    # delete does not require waiting. it has no consistency level.



def execute(command, timestamp, src_addr):
    """ Execute a command either from the command prompt or from a message.
        This actually does the execution on this server -- not message passing and waiting """

    if is_get(command):
        print "executing get on this machine"
        key = command_parser.get_key(command)
        value = globes.db.get(key)
        send_reply(value, timestamp, src_addr)

    elif is_insert(command):
        print "executing insert on this machine"
        key = command_parser.get_key(command)
        value = command_parser.get_value(command)
        globes.db.insert(key, value)
        send_reply("successfully inserted", timestamp, src_addr)

    elif is_update(command):
        print "executing update on this machine"
        key = command_parser.get_key(command)
        value = command_parser.get_value(command)
        globes.db.update(key, value)
        send_reply("successfully updated", timestamp, src_addr)

    elif is_delete(command):
        print "executing delete on this machine"
        key = command_parser.get_key(command)
        globes.db.delete(key)
    else:
        return False

    return True



def recv_command_thread(args):
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

    start_new_thread( recv_command_thread, ("no args",) )

    print "***** Enter a command *****"
    while True:
        command = raw_input(">>>")
        time = create_timestamp()
        process_input(command, time)



if __name__ == "__main__":
    main(sys.argv[1:])

