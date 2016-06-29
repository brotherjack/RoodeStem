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
            