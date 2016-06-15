'''
Created on Jun 13, 2016

@author: Thomas Adriaan Hellinger

Utility file for operations that are useful across modules and packages.
'''
def flatten(l): 
    """Flattens a list into 1-dimension"""
    return flatten(l[0]) +\
        (flatten(l[1:]) if len(l) > 1 else []) if type(l) is list else [l]

def listize(x):
    """Returns a list with a thing in it, unless the thing is already a list"""
    return [x] if type(x) is not list else x

def safe_list_append(x,y):
    """Appends a list of x to a list of y"""
    return listize(x) + listize(y) 