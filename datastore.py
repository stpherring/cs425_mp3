""" A key-value datastore.  The datastore supports the following operations:
        get, insert, update, delete """

import globes

class Datastore:

    def __init__(self):
        self.db = dict()


    def get(self, key, level):
        print "getting " + str(key)


    def insert(self, key, value, level):
        print "inserting (" + str(key) + ", " + str(value) + ")"


    def update(self, key, value, level):
        print "updating (" + str(key) + ", " + str(value) + ")"


    def delete(self, key):
        print "deleting " + str(key)