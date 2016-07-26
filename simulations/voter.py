'''
Created on Jul 25, 2016

@author: Thomas Adriaan Hellinger
'''
from abc import ABCMeta, abstractmethod
from math import sqrt, pow


class Voter(object):
    def __init__(self, voting_metric):
        self.metric = voting_metric

    def determine_opinion_on(self, vm, rng=(0,10)):
        if type(vm is Voter):
            return self.metric.determine_distance_from(vm.metric, rng)
        else:
            return self.metric.determine_distance_from(vm, rng)

class VotingMetric(object, metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, **kwargs):
        pass
    
    @property
    def dimensions(self):
        return self._dimensions
    
    def get_axis_labels(self):
        return self._dimensions.keys()
    
    @property
    def cardinality(self):
        return self._cardinality
    
    @abstractmethod
    def determine_distance_from(self, dim):
        pass


class NolanChart(VotingMetric):
    MAX_DISTANCE = sqrt(8)
    def __init__(self, public_auth, pri_prop):
        self._dimensions = {"public_authority": public_auth, 
                            "private_property": pri_prop}
        for score, pos in self._dimensions.items(): 
            if pos < -1 or pos > 1:
                msg = "Voter position must be within [-1, 1]."
                msg += " Score for {0} is {1}."
                raise TypeError(msg.format(score, pos))
        self._cardinality = 2  


    def determine_distance_from(self, vm, rng):
        if rng[1] <= rng[0]:
            msg = "Max rng: {0} must be GREATER THAN min rng: {1}"
            raise TypeError(msg.format(rng[1], rng[0]))
        
        sm = 0
        for k in self.get_axis_labels():
            sm += pow(self._dimensions[k] - vm.dimensions[k], 2)
        sm = sqrt(sm / pow(NolanChart.MAX_DISTANCE, 2))
        return rng[1] - rng[1]*sm 