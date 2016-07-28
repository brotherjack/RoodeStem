'''
Created on Jul 25, 2016

@author: Thomas Adriaan Hellinger
'''
import pytest

from roodestem.simulations.voter import( 
    Voter,
    VotingMetric,
    NolanChart, 
    Thomas_Adriaan_Hellinger,
    us_presidential_candidates_2016
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
        
class TestVotingMetric:
    def test_voting_metric_abstract(self):
        with pytest.raises(TypeError):
            vm = VotingMetric()
    
    def test_cannot_delete_cardinality(self):
        cn = NolanChart(0,0)
        with pytest.raises(AttributeError):
            del cn.cardinality
    
    def test_cannot_change_cardinality(self):
        cn = NolanChart(0,0)
        with pytest.raises(AttributeError):
            cn.cardinality = 3
    
    def test_cannot_compare_different_voting_metrics(self):
        class SomeDumbMetric(VotingMetric):
            def __init__(self, *kwargs):
                return
            def determine_distance_from(self, dim):
                return 'BURP!'
            
        with pytest.raises(TypeError):
            voter = Voter(NolanChart(0,0))
            candidate = Voter(SomeDumbMetric())
            voter.determine_opinion_on(candidate)
            
        
class TestNolanChart:
    def test_tommy_is_a_commie(self):
        assert(
            Thomas_Adriaan_Hellinger.metric.position == "libertarian leftist"
        )
    
    def test_donald_trump_is_a_dick(self):
        trump = [
            x for x in us_presidential_candidates_2016\
            if x.name == 'Donald Trump'
        ][0]
        assert(trump.metric.position == "authoritarian rightist")
    
    def test_hillary_clinton_is_also_a_dick(self):
        clinton = [
            x for x in us_presidential_candidates_2016\
            if x.name == 'Hillary Clinton'
        ][0]
        assert(clinton.metric.position == "authoritarian rightist")
    
    def test_gary_johnson_is_kinda_a_dick(self):
        johnson = [
            x for x in us_presidential_candidates_2016\
            if x.name == 'Gary Johnson'
        ][0]
        assert(johnson.metric.position == "libertarian rightist")
    
    def test_bernie_sanders_is_not_a_commie(self):
        sanders = [
            x for x in us_presidential_candidates_2016\
            if x.name == 'Bernie Sanders'
        ][0]
        assert(sanders.metric.position == "centrist")
    
    def test_joseph_stalin_is_a_leftist_dick(self):
        stalin = Voter(NolanChart(1, -.3))
        assert(stalin.metric.position == 'authoritarian leftist')
    
    def test_for_theoretical_just_leftist(self):
        somebody = Voter(NolanChart(0,-1))
        assert(somebody.metric.position == 'leftist')
    
    def test_for_theoretical_just_rightist(self):
        somebody = Voter(NolanChart(0,1))
        assert(somebody.metric.position == 'rightist')
    
    def test_for_theoretical_just_authoritarian(self):
        somebody = Voter(NolanChart(1,0))
        assert(somebody.metric.position == 'authoritarian')
    
    def test_for_theoretical_just_libertarian(self):
        somebody = Voter(NolanChart(-1,0))
        assert(somebody.metric.position == 'libertarian')
    
    def test_for_theoretical_super_centrist(self):
        somebody = Voter(NolanChart(0,0))
        assert(somebody.metric.position == 'centrist') 
    
    def test_bad_dimensions(self):
        bad_dims = [(2,-2),(0,-2),(-2,0),(0,2),(2,0),(-2,2),(2,2),(-2,-2)]
        for x,y in bad_dims:
            with pytest.raises(AttributeError):
                nc = NolanChart(x,y)
        