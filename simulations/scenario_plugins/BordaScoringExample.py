'''
Created on Jul 6, 2016

@author: Thomas Adriaan Hellinger
'''
from functools import wraps
from importlib import import_module

from yapsy.IPlugin import IPlugin

from simulations.scenarios import Scenario


class BordaScoringExample(Scenario, IPlugin):
    def __init__(self, choices=['a','b','c', 'd']):
        self._choices = choices
        self.mods = [
            ('voting_systems.borda', 'BordaCount'), 
            ('voting_systems.voting_system', 'OrdinalVote'),
            ('random',) 
        ]
    
    
    def _import(self):
        for mod in self.mods:
            if len(mod) > 1:
                module = __import__(mod[0], fromlist=mod[1:])
                for cls in mod[1:]:
                    globals()[cls] = getattr(module, cls)
            else:
                globals()[mod[0]] = import_module(mod[0])

    def run(self, rn=10):
        self._import()
        for r in range(0, rn):
            print("Choices are: {0}".format(self.choices))
            votes = []
            random.seed(r)
            randselects = [random.randint(0,1) for _ in range(0, 100)]
            for i in range(0, 50): 
                if randselects[i] == 0:
                    votes.append(OrdinalVote(['a', 'b', 'c', 'd']))
                else:
                    votes.append(OrdinalVote(['a', 'c', 'b', 'd']))
            
            for i in range(50, 100):
                if randselects[i] == 0:
                    votes.append(OrdinalVote(['d', 'b', 'c', 'a']))
                else:
                    votes.append(OrdinalVote(['d', 'c', 'b', 'a']))
    
            bc = BordaCount(self.choices,
                            score_fn=BordaCount.fractional_score_function)
            print("bc is {0}".format(bc))
            results = bc.decide(votes)
            msg = "Results with fractional scoring fn: {0}\nScores: {1}"
            print(msg.format(results, bc.scores))

            bc = BordaCount(self.choices)
            print("bc is {0}".format(bc))
            results = bc.decide(votes)
            msg = "Results with standard scoring fn: {0}\nScores: {1}"
            print(msg.format(results, bc.scores))
            
    @property
    def description(self):
        return cls.description()
    
    @property
    def choices(self):
        return self._choices
    
    @choices.setter
    def choices(self, choices):
        self._choices = choices
    
    def __repr__(self):
        return "<RandomCondorcet: choices={0}>".format(self.choices)