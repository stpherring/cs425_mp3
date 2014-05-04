from utils import *
from command_parser import *

def search(key):
    """ This should not be a separate file. It is right now to avoid merging """
    """ Send a get request to all replicas. Do not do read repair. """

    ## just copy paste get all
    ## wait for all responses and then print out all the keys
    ## but do NOT do read repair