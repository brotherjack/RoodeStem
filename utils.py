'''
Created on Jun 13, 2016

@author: Thomas Adriaan Hellinger
'''

def safe_list_append(x,y):
    if type(x) is list:
        if type(y) is list:
            return x + y
        else:
            return x + [y]
    else:
        if type(y) is list:
            return [x] + y 
        else:
            return [x] + [y]

def flatten(l): 
    return flatten(l[0]) +\
        (flatten(l[1:]) if len(l) > 1 else []) if type(l) is list else [l]
