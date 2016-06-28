#!/usr/bin/env python3
from abc import abstractmethod, ABCMeta
from itertools import combinations

from utils import flatten, listize, safe_list_append


class VotingException(Exception): pass
class VotingError(Exception): pass


class Result:
    _condtypes = ['winner', 'loser', 'tied']
    def __init__(self, **order):
        for cond in Result._condtypes:
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
    
    @staticmethod
    def _cmp_type(r, ty):
        return set(listize(getattr(r, ty)))
    
    def __eq__(self, other):
        for ty in Result._condtypes:
            if not Result._cmp_type(self, ty) == Result._cmp_type(other, ty):
                return False
        return True          
    
    def __repr__(self):
        if self._tied:
            return "<Result(tied={0})>".format(self._tied)
        else:
            return "<Result(winner={0}, loser={1})>".format(self._winner,
                                                            self._loser)


class VotingSystem(object, metaclass=ABCMeta):
    def __init__(self, choices):
        if len(choices) < 2:
            raise VotingError("A voting system requires two or more choices.")

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

    def _return_results(self, results):
        desclist = sorted(results.items(), key=lambda x: x[1], reverse=True)
        res, bar = Result.ord_items(desclist[0], desclist[1])
        for itm in desclist[2:]:
            if itm[1] > bar:
                res.loser = safe_list_append(res.winner, res.loser)
                res.winner = itm[0]
                bar = itm[1]
            elif itm[1] < bar:
                res.loser = safe_list_append(itm[0], res.loser)
            else:
                res.winner = safe_list_append(res.winner, itm[0])
        return res

class OrdinalSystem(VotingSystem):
    def __init__(self, choices):
        super().__init__(choices)

    @property
    def is_ordinal(self):
        return True

    
class CardinalSystem(VotingSystem):
    def __init__(self, choices):
        super().__init__(choices)

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

    def __iter__(self):
        return iter(self._choices)
    
    def __len__(self):
        return len(self._choices)

    def __repr__(self):
        return "<OrdinalVote: {0}>".format(self._choices)

class CardinalVote(Vote):
    @property    
    def choices(self):
        return self._choices

        