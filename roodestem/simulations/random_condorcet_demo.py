'''
Created on Jul 5, 2016

@author: Thomas Adriaan Hellinger
'''
import random

from voting_systems.condorcet import CondorcetMethod, CondorcetParadox
from voting_systems.voting_system import OrdinalVote
from simulations.scenarios import Scenario


class RandomCondorcetDemo(Scenario):
    def __init__(self, choices=['a','b','c', 'd']):
        self._choices = choices
    
    def run(self, rn=10):
        cm = CondorcetMethod(self.choices)
        votes = [
            OrdinalVote(
                random.sample(self.choices, len(self.choices))) 
                for i in range(0, rn)
        ]
        results = ""
        results = cm.decide(votes, verbose=True,
                            colors=["red", "blue", "green", "yellow"])
        return {
            "choices": self.choices,
            "votes": [v.choices for v in votes],
            "results" : "{0}".format(results['results']),
            "msgs": results['msgs']
        }
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
        return "<RandomCondorcetDemo: choices={0}>".format(self.choices)