'''
Created on Jul 25, 2016

@author: Thomas Adriaan Hellinger
'''
import pytest

from roodestem.simulations.voter import( 
    Voter,
    NolanChart, 
    Thomas_Adriaan_Hellinger
)


class TestVoter:
    def test_identical_opinions(self):
        v1 = Voter(NolanChart(0, 0))
        v2 = Voter(NolanChart(0, 0))
        assert(v1.determine_opinion_on(v2) == 10)
    
    def test_polar_opposite_opinions(self):
        v1 = Voter(NolanChart(-1, -1))
        v2 = Voter(NolanChart(1, 1))
        assert(v1.determine_opinion_on(v2) < 1e-9)
        
class TestNolanChart:
    def test_tommy_is_a_commie(self):
        assert(Thomas_Adriaan_Hellinger.metric.position == "libertarian leftist")
        