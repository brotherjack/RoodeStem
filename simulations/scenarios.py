'''
Created on Jun 29, 2016

@author: Thomas Adriaan Hellinger
'''
from abc import ABCMeta, abstractmethod
from functools import wraps

from importlib import import_module


class Scenario(object, metaclass=ABCMeta):

    @abstractmethod
    def run(self):
        pass
    
    @property
    @abstractmethod
    def description(self):
        pass
    

class RandomCondorect(Scenario):
    def __init__(self, choices):
        self.choices = choices
        
    @staticmethod
    def _import(mods):
        #embed()
        for mod in mods:
            if len(mod) > 1:
                module = __import__(mod[0], fromlist=mod[1:])
                for cls in mod[1:]:
                    globals()[cls] = getattr(module, cls)
            else:
                globals()[mod[0]] = import_module(mod[0])

    def run(self, mods, rn=10):
        self._import(mods)
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
    
    def __repr__(self):
        return "<RandomCondorcet: choices={0}>".format(self.choices)