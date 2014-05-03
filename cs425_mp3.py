
DELAYS {}
SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def execute(command):
    """Execute a user specified command"""
    params = command.split(" ")
    action = params[0]
    key = params[0]

    if action == "delete":
        delete(key)
    if action == "get":
        level = int(params[2])
        get(key, level)
    elif action == "insert":
        value = params[2]
        level = int(params[3])
        insert(key, value, level)
    elif action == "update":
        value = params[2]
        level = int(params[3])
        update(key, value, level)
    else:
        print "Invalid command"

def recv_thread(args):
    """ Thread that recv's new messages """
    while True:
        addr, message = receive()

        """We want to split the message up in the following format:
            delete*key
            get*key*level
            insert*key*value*level
            update*key*value*level
            
            This requires some trivial string parsing"""
        message_components = message.split("*")

        action = message_components[0]
        key = int(message_components[1])
        if action == "delete":
            delete(key)
        if action == "get":
            level = int(message_components[2])
            get(key, level)
        elif action == "insert":
            value = message_components[2]
            level = int(message_components[3])
            insert(key, value, level)
        elif action == "update":
            value = message_components[2]
            level = int(message_components[3])
            update(key, value, level)
        else:
            print "Error in recv: " + action + " not a valid action"


def receive():
    """We will split addr from content with # and message components with * """
    content, addr = SOCK.recvfrom(4096)
    components = content.split("#")

    addr = components[0]
    message = components[1]

    return addr, message


def read_config_file(config_file_name):
    """ Read the config file and return an array of IP addrs"""
    with open(config_file_name) as config_file:
        ip_addrs = config_file.readlines()
        # Remove trailing \n
        ip_addrs = [addr.strip() fro addr in ip_addrs]
        global TERMINAL_ID
        TERMINAL_ID = ip_addrs.pop(0)
    return ip_addrs

def main(argv):
    """ Get command line args """
    if len(argv) >= 1:
        config_file_name = argv(0)
    else:
        print "Usage: python2 cs425_mp3.py <configfile> <avg_delay_1>...<avg_delay_n-1>"
        sys.exit(2)

    """ Read config file.  File should contain n IP addrs"""
    ip_addrs = read_config_file(config_file_name)
    global DELAYS
    i = 1
    for addr in ip_addrs:
        DELAYS[addr] = argv(i)
        i += 1
    try:
        global TERMINAL_ID
        SOCK.bind(parse_addr(ip_addrs[TERMINAL_ID]))
    except socket.error, msg:
        print "Bind failed. Error Code: " + str(msg[0]) + " Message: " + msg[1]
        sys.exit()

    start_new_thread(recv_thread()
    print "***** Enter a command *****"

    while True:
        command = raw_input("")
        execute(command)

# Run main
if __name == "__main__":
    main(sys.argv[1:])
