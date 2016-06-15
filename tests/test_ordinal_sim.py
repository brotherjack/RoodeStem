'''
Created on Jun 10, 2016

@author: Thomas Adriaan Hellinger
'''
import pytest

import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
print(os.listdir(myPath + '/../'))

from voting_systems.voting_system import OrdinalSystem, OrdinalVote
from voting_systems.condorcet import CondorcetMethod, CondorcetParadox


class TestOrdinal:
    
    def test_ordinal_system_is_abstract(self):
        with pytest.raises(TypeError):
            ordsys = OrdinalSystem()

    def test_condercet_paradox(self):
        with pytest.raises(CondorcetParadox):
            cm = CondorcetMethod(['a', 'b', 'c'])
            votes = [
                OrdinalVote(['a','b','c']),
                OrdinalVote(['b','c','a']),
                OrdinalVote(['c','a','b'])
            ]
            cm.decide(votes)