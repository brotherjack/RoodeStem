'''
Created on Jun 10, 2016

@author: Thomas Adriaan Hellinger
'''
from IPython import embed

from voting_systems.condorcet import CondorcetMethod, CondorcetParadox
from voting_systems.voting_system import OrdinalVote

if __name__ == '__main__':
    from voting_systems.condorcet import CondorcetMethod, CondorcetParadox
    from voting_systems.voting_system import OrdinalVote
    a = 'a'
    b = 'b'
    c = 'c'
    d = 'd'
    e = 'e'

    import random
    choices = [a,b,c,d,e]
    print("Choices are: {0}".format(choices))
    cm = CondorcetMethod(choices)
    print("cm is {0}".format(cm))
    votes = [OrdinalVote(random.sample(choices, 5)) for i in range(0, 10)]
    for i, vote in enumerate(votes):
        print("vote[{0}]: {1}".format(i,vote))

    try:
        results = cm.decide(votes)
        print("results are: {0}".format(results))
    except CondorcetParadox as cp:
        print(cp.msg)
    
    embed()
