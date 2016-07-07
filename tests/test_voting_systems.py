'''
Created on Jun 29, 2016

@author: Thomas Adriaan Hellinger
'''
import pytest

from voting_systems.voting_system import Result


class TestResult:
    
    def test_null_result_not_tolerated(self):
        with pytest.raises(TypeError):
            Result()
    
    def test_passed_multiple_winners(self):
        res = Result(winner=['a', 'b', 'c'], tied=['b','c'])
        assert res == Result(tied=['a', 'b', 'c'])
    
    def test_passed_all_losers(self):
        res = Result(loser=['a', 'b', 'c'])
        assert res == Result(tied=['a', 'b', 'c'])
    
    def test_passed_all_winners(self):
        res = Result(winner=['a', 'b', 'c'])
        assert res == Result(tied=['a', 'b', 'c'])