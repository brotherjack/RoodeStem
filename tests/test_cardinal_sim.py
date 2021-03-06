'''
Created on Jun 15, 2016

@author: Thomas Adriaan Hellinger
'''
import pytest

from roodestem.voting_systems.voting_system import(
    CardinalSystem, 
    OrdinalVote,
    CardinalVote, 
    Result,
    VotingError,
)
from roodestem.voting_systems.borda import BordaCount
from roodestem.voting_systems.ranked import RankedBallot
from roodestem.voting_systems.plurality import PluralityBallot


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

class TestRankedBallot:    
    def test_ranked_ballot_score_bounds_checking(self):
        with pytest.raises(TypeError):
            rb = RankedBallot(['a', 'b', 'c'], (10, 0))
    
    def test_simple_ranked_ballot_scenario(self):
        rng = (0, 10) 
        rb = RankedBallot(['a', 'b', 'c'], rng)
        votes = [
            CardinalVote({'a': 10, 'b': 5, 'c': 0}, rng),
            CardinalVote({'a': 7, 'b': 3, 'c': 1}, rng),
            CardinalVote({'a': 2, 'b': 0, 'c': 0}, rng),
        ]
        res = rb.decide(votes)
        assert(res.winner == 'a')
    
    def test_simple_ranked_ballot_tied_scenario(self):
        rng = (0, 10) 
        rb = RankedBallot(['a', 'b', 'c'], rng)
        votes = [
            CardinalVote({'a': 10, 'b': 10, 'c': 0}, rng),
            CardinalVote({'a': 10, 'b': 10, 'c': 1}, rng),
            CardinalVote({'a': 10, 'b': 10, 'c': 0}, rng),
        ]
        res = rb.decide(votes)
        assert('a' in res.tied and 'b' in res.tied and 'c' in res.loser)

class TestPlurality:
    def test_simple_plurality_ballot_scenario(self):
        pb = PluralityBallot(['a', 'b', 'c'])
        rng = (0,1)
        votes = [
            CardinalVote({'a': 1, 'b': 0, 'c': 0}, rng),
            CardinalVote({'a': 1, 'b': 0, 'c': 0}, rng),
            CardinalVote({'a': 0, 'b': 0, 'c': 1}, rng),
        ]
        res = pb.decide(votes)
        assert(res.winner == 'a')
    
    
    def test_plurality_ballot_allows_only_one_choice(self):
        with pytest.raises(VotingError):
            pb = PluralityBallot(['a', 'b', 'c'])
            rng = (0,1)
            votes = [
                CardinalVote({'a': 1, 'b': 0, 'c': 0}, rng),
                CardinalVote({'a': 1, 'b': 0, 'c': 1}, rng),
                CardinalVote({'a': 0, 'b': 0, 'c': 1}, rng),
            ]
            res = pb.decide(votes)
            
    def test_abstain_on(self):
        pb = PluralityBallot(['a', 'b', 'c'], can_abstain=True)
        rng = (0,1)
        votes = [
            CardinalVote({'a': 1, 'b': 0, 'c': 0}, rng),
            CardinalVote({'a': 1, 'b': 0, 'c': 0}, rng),
            CardinalVote({'a': 0, 'b': 0, 'c': 0}, rng),
            CardinalVote({'a': 0, 'b': 0, 'c': 1}, rng),
        ]
        res = pb.decide(votes)
        assert(res.winner == 'a')
    
    def test_abstain_off(self):
        with pytest.raises(VotingError):
            pb = PluralityBallot(['a', 'b', 'c'], can_abstain=False)
            rng = (0,1)
            votes = [
                CardinalVote({'a': 1, 'b': 0, 'c': 0}, rng),
                CardinalVote({'a': 0, 'b': 0, 'c': 0}, rng),
                CardinalVote({'a': 0, 'b': 0, 'c': 1}, rng),
            ]
            res = pb.decide(votes)