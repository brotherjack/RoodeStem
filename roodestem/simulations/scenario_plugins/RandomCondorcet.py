'''
Created on Jul 5, 2016

@author: Thomas Adriaan Hellinger
'''
from functools import wraps
from importlib import import_module

from yapsy.IPlugin import IPlugin

from simulations.scenarios import Scenario


class RandomCondorcet(Scenario, IPlugin):
    def __init__(self, choices=['a','b','c', 'd']):
        self._choices = choices
        self.mods = [
            ('voting_systems.condorcet', 'CondorcetMethod', 'CondorcetParadox'), 
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
        print("Choices are: {0}".format(self.choices))
        cm = CondorcetMethod(self.choices)
        print("cm is {0}".format(cm))
        votes = [
            OrdinalVote(
                random.sample(self.choices, len(self.choices))) 
                for i in range(0, rn)
        ]
        for i, vote in enumerate(votes):
            print("vote[{0}]: {1}".format(i,vote))
    
        try:
            results = cm.decide(votes)
            print("results are: {0}".format(results))
        except CondorcetParadox as cp:
            print(cp.msg)
    
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