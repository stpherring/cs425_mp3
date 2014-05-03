""" Implementation of the four key-value store commands:
        get, insert, update, delete """

import globes


def get(key, level):
    print "getting " + str(key)


def insert(key, value, level):
    print "inserting (" + str(key) + ", " + str(value) + ")"


def update(key, value, level):
    print "updating (" + str(key) + ", " + str(value) + ")"


def delete(key):
    print "deleting " + str(key)