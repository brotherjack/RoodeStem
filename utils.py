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
