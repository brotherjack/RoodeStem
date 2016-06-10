'''
Created on Jun 10, 2016

@author: Thomas Adriaan Hellinger
'''
from voting_systems.condorcet import CondorcetMethod, CondorcetParadox
from voting_systems.voting_system import OrdinalVote

if __name__ == '__main__':
    a = 'a'
    b = 'b'
    c = 'c'
    d = 'd'
    e = 'e'

    import random
    choices = [a,b,c,d,e]
    cm = CondorcetMethod(choices)
    votes = [OrdinalVote(random.sample(choices, 5)) for i in range(0, 10)]
    try:
        print(cm.decide(votes))
    except CondorcetParadox as cp:
        print(cp.msg)
