""" A class of helper functions to parse a command """


def get_action(command):
    """ Extract the action from a command (get, insert, update, delete) """
    return command.split(" ")[0]

def get_key(command):
    """ Extract the key from a command """
    return command.split(" ")[1]

def get_value(command):
    """ Extract the 'value' from a command """
    if is_get(command) or is_delete(command):
        return None
    elif is_insert(command) or is_update(command):
        command.split(" ")[2]

def get_level(command):
    """ Extract the 'value' from a command """
    if is_delete(command):
        return None
    elif is_get(command):
        return int(command.split(" ")[2])
    elif is_insert(command) or is_update(command):
        return int(command.split(" ")[3])



def is_valid_command(command):
    """ Given a command, return True if it is valid, else False """
    return is_get(command) or is_insert(command) or is_update(command) or is_delete(command)

""" Helper functions to determine what type of command it is """
def is_get(command):
    params = command.split(" ")
    return params[0] == "get" and len(params) == 3
def is_insert(command):
    params = command.split(" ")
    return params[0] == "insert" and len(params) == 4
def is_update(command):
    params = command.split(" ")
    return params[0] == "update" and len(params) == 4
def is_delete(command):
    params = command.split(" ")
    return params[0] == "delete" and len(params) == 2
