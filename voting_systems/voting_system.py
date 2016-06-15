#!/usr/bin/env python3
from abc import abstractmethod, ABCMeta
from itertools import combinations

from utils import flatten

class VotingException(Exception): pass
class VotingError(Exception): pass


def flatten(l): 
    return flatten(l[0]) +\
        (flatten(l[1:]) if len(l) > 1 else []) if type(l) is list else [l]


class Result:
    def __init__(self, **order):
        for cond in ['winner', 'loser', 'tied']:
            setattr(self, cond, order.get(cond, []))
    
    @property  
    def winner(self):
        return self._winner

    @property  
    def loser(self):
        return self._loser

    @property  
    def tied(self):
        return self._tied
    
    
    @winner.setter  
    def winner(self, value):
        self._winner = value

    @loser.setter  
    def loser(self, value):
        self._loser = value

    @tied.setter  
    def tied(self, value):
        self._tied  = value
    
    @classmethod
    def ord_items(cls, x, y):
        if x[1] > y[1]:
            return (cls(winner=x[0],loser=y[0]), x[1])
        elif x[1] < y[1]:
            return (cls(winner=y[0], loser=x[0]), y[1])
        else:
            return (cls(winner=[x[0], y[0]]), x[1])
    
    def __repr__(self):
        if self._tied:
            return "<Result(tied={0})>".format(self._tied)
        else:
            return "<Result(winner={0}, loser={1})>".format(self._winner,
                                                            self._loser)


class VotingSystem(object, metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, choices):
        pass

    @property
    @abstractmethod #TODO: Note explaining why not abstractmethod > property as blog post
    def choices(self):
        pass

    @property
    @abstractmethod
    def is_ordinal(self):
        pass


    @abstractmethod
    def decide(self, votes):
        pass


class OrdinalSystem(VotingSystem):
    @property
    def is_ordinal(self):
        return True

    
class CardinalSystem(VotingSystem):
    @property
    def is_ordinal(self):
        return False


class Vote(metaclass=ABCMeta):
    def __init__(self, choices):
        self._choices = choices
        
    @property
    @abstractmethod
    def choices(self):
        pass

class OrdinalVote(Vote):
    def __init__(self, choices):
        #super()
        self._choices = choices
        choices = flatten(choices)
        if len(choices) != len(set(choices)):
            dupes = set(filter(lambda yi: y.count(yi) > 1, y))
            msg = "{0} has the following option {1} more than once."
            raise VotingError(msg.format(self._choices, dupes))

    @property    
    def choices(self):
        return self._choices

    def ranking(self, choice):
        return self.choices.index(choice)

    def __repr__(self):
        return "<OrdinalVote: {0}>".format(self._choices)

class CardinalVote(Vote):
    @property    
    def choices(self):
        return self._choices

        