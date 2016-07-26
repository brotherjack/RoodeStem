'''
Created on Jul 25, 2016

@author: Thomas Adriaan Hellinger
'''
import pytest

from simulations.voter import Voter, NolanChart


class TestVoter:
    def test_identical_opinions(self):
        v1 = Voter(NolanChart(0, 0))
        v2 = Voter(NolanChart(0, 0))
        assert(v1.determine_opinion_on(v2) == 10)
    
    def test_polar_opposite_opinions(self):
        v1 = Voter(NolanChart(-1, -1))
        v2 = Voter(NolanChart(1, 1))
        assert(v1.determine_opinion_on(v2) < 1e-9)