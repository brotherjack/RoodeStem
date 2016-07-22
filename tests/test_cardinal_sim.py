'''
Created on Jun 15, 2016

@author: Thomas Adriaan Hellinger
'''
import pytest

from voting_systems.voting_system import(
    CardinalSystem, 
    OrdinalVote,
    CardinalVote, 
    Result,
    VotingError,
)
from voting_systems.borda import BordaCount


class TestCardinal:
    
    def test_cardinal_system_is_abstract(self):
        with pytest.raises(TypeError):
            cardsys = CardinalSystem()
    
    def test_cardinal_vote_instantiation(self):
        cv = CardinalVote({'a':0, 'b':5, 'c':10}, (0,10))
        assert(type(cv) == CardinalVote)
    
    def test_cardinal_vote_out_of_range(self):
        with pytest.raises(VotingError):
            cv = CardinalVote({'a':0, 'b':5, 'c':100}, (0,10))
    
    def test_cardinal_range_set(self):
        with pytest.raises(TypeError):
            cv = CardinalVote({'a':0, 'b':5, 'c':10}, (10,0))
        

class TestBordaCount:
    def test_borda_count(self):
        votes = [OrdinalVote(['a', 'b', 'c'])]
        bc = BordaCount(['a', 'b', 'c'])
        result = bc.decide(votes)
        expected_result = Result(winner='a', loser=['b','c'])
        assert(result == expected_result)
    
    def test_respond_correctly_to_one_choice(self):
        with pytest.raises(VotingError):
            bc = BordaCount(['a'])
    
    def test_fractional_scoring_function(self):
        bc = BordaCount(['a', 'b', 'c'], BordaCount.fractional_score_function)
        bc.decide([OrdinalVote(['a', 'b', 'c'])])
        assert bc.scores['a'] == 1 and bc.scores['b'] == 0.5 and (
            bc.scores['c'] > 0.32 and  bc.scores['c'] < 0.34)
        
    def test_result_matches_scoring(self):
        bc = BordaCount(['a', 'b', 'c'], BordaCount.fractional_score_function)
        result = bc.decide([OrdinalVote(['a', 'b', 'c'])])
        expected_result = Result(winner='a', loser=['b', 'c'])
        assert(result == expected_result)
    
    def test_result_of_more_than_3(self): 
        bc = BordaCount(['a', 'b', 'c', 'd'])
        result = bc.decide([OrdinalVote(['a', 'b', 'c', 'd'])])
        expected_result = Result(winner='a', loser=['b', 'c', 'd'])
        assert(result == expected_result)
    
    def test_reset_score_default(self):
        bc = BordaCount(['a', 'b'])
        bc.decide([OrdinalVote(['a', 'b'])])
        # Now decide again, scores should reset
        bc.decide([OrdinalVote(['a', 'b'])])
        assert(bc.scores['a'] == 1 and bc.scores['b'] == 0) 
        
    def test_reset_score_optional(self):
        bc = BordaCount(['a', 'b'])
        bc.decide([OrdinalVote(['a', 'b'])])
        # Now decide again, scores should NOT reset
        bc.decide([OrdinalVote(['a', 'b'])], reset_scores=False)
        assert(bc.scores['a'] == 2) 