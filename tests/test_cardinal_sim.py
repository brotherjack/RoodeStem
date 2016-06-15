'''
Created on Jun 15, 2016

@author: Thomas Adriaan Hellinger
'''
import pytest

import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
print(os.listdir(myPath + '/../'))

from voting_systems.voting_system import CardinalSystem, OrdinalVote, Result
from voting_systems.borda import BordaCount


class TestCardinal:
    
    def test_cardinal_system_is_abstract(self):
        with pytest.raises(TypeError):
            cardsys = CardinalSystem()
    
    def test_borda_count(self):
        votes = [OrdinalVote(['a', 'b', 'c']), OrdinalVote(['a', 'b', 'c'])]
        bc = BordaCount(['a', 'b', 'c'])
        result = bc.decide(votes)
        expected_result = Result(winner='a', loser=['b','c'])
        assert(result == expected_result) 