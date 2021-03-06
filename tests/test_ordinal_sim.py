'''
Created on Jun 10, 2016

@author: Thomas Adriaan Hellinger
'''
import pytest
    
from roodestem.voting_systems.voting_system import (
    OrdinalSystem, 
    OrdinalVote, 
    VotingError,
)
from roodestem.voting_systems.condorcet import CondorcetMethod, CondorcetParadox


class TestOrdinal:
    
    def test_ordinal_system_is_abstract(self):
        with pytest.raises(TypeError):
            ordsys = OrdinalSystem()

    def test_condercet_paradox(self):
        cm = CondorcetMethod(['a', 'b', 'c'])
        votes = [
            OrdinalVote(['a','b','c']),
            OrdinalVote(['b','c','a']),
            OrdinalVote(['c','a','b'])
        ]
        decision = cm.decide(votes)
        assert(decision['results'].startswith("Detected cycle"))
    
    def test_respond_correctly_to_one_choice(self):
        with pytest.raises(VotingError):
            cm = CondorcetMethod(['a'])
        