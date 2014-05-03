""" A key-value datastore.  The datastore supports the following operations:
        get, insert, update, delete """

import globes

class Datastore:

    def __init__(self):
        self.kv_store = dict()


    def get(self, key):
        print "getting " + str(key)
        return self.kv_store[key]

    def insert(self, key, value):
        print "inserting (" + str(key) + ", " + str(value) + ")"
        self.kv_store[key] = value


    def update(self, key, value):
        print "updating (" + str(key) + ", " + str(value) + ")"
        if key in kv_store:
            self.kv_store[key] = value

    def delete(self, key):
        print "deleting " + str(key)
        del self.kv_store[key]


    def repair(self, key):
        """ Performs a repair on the key across all replicas containing the key """
        print "repairing " + str(key)
        all_replicas = all_replica_nums(key)

    def show_all():
        print self.kv_store
