'''
Created on Jun 10, 2016

@author: Thomas Adriaan Hellinger
'''
from IPython import embed

from simulations.scenarios import RandomCondorcet 

if __name__ == '__main__':
    rc = RandomCondorcet(['a','b','c','d'])
    rc.run([
            ('voting_systems.condorcet', 'CondorcetMethod', 'CondorcetParadox'), 
            ('voting_systems.voting_system', 'OrdinalVote'), 
            ('random',)
    ])
    embed()
