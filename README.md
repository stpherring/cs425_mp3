
CS 425 MP3

A distributed key-value store implemented in Python.


Will Hennessy    -- whennes2
Stephen Herring  -- sgherri2



EXECUTION

If you wish to run this distributed datastore on 4 servers, then take the following steps:
  1) in config.json, enter 4 different addresses and create a 4x4 array of avg delay times
  2) in four separate terminals, execute
        python2 mp3.py 0
        python2 mp3.py 1
        python2 mp3.py 2
        python2 mp3.py 3

This extends to an arbitrary number of servers in the obvious way.



INPUT COMMANDS

The datastore supports the following six operations:
  - get key level
        returns the value of that key in the datastore
        performs a read-repair when necessary (further detail below)
  - insert key value level
        inserts the key-value pair into the datastore
  - update key value level
        updates the key-value pair in the datastore
  - delete key
        removes the key-value pair from all replicas in the datastore
  - show-all
        prints all key-value pairs in the specified server's datastore
        does not perform a read-repair
  - search key
        prints the key-value pairs of the corresponding key at each server in the system
        does not perform a read-repair



IMPLEMENTATION

Each server in the system has two sockets: command_sock and reply_sock.
Command_sock is used to send and receive command messages like get and insert.
Reply_sock is used to send and receive reply message like value=2 and insert successful.
Each server has a background thread listening for incoming commands on command_sock.
Each server accepts user input from the terminal

Our system implements read-repair in order to maintain eventual consistency.
When a get command is executed, a command message is sent to every server containing the key.
After all servers have returned their value, the coordinator server will compare the
timestamp (an attribute of the value) of each returned value. If they do not all share the same timestamp, then the coordinator will choose the one with the latest timestamp.
Finally, the coordinator will send an update message to every server to update their value
to the chosen value.

The datastore is implemented as a simple key-value store.
key => (value, timestamp)
The datastore is a Python-defined class with a dictionary attribute and all the 
appropriate functionalities:  get, insert, update, delete, show-all


