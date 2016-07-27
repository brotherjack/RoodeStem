#!/usr/bin/env python3
from abc import abstractmethod, ABCMeta
from itertools import combinations

from utils import flatten, listize, safe_list_append


class VotingException(Exception): pass
class VotingError(Exception): pass


class Result:
    """The outcome of a round of voting, with winners, losers, and ties.
    
    An immutable object which contains the outcome of a single round of voting.
    Values passed to the Result constructor may be changed if not logically
    consistent. See :func:`Result._resolve_incorrect_states_on_init` for more
    details.

    Args: 
        winner (:obj:`str`, optional): A single winner labeled with a string.
        tied (:obj:`list` of :obj:`str`, optional): In the case of multiple 
            winners, this parameter contains the label of all tied candidate 
            options.
        loser (:obj:`list` of :obj:`str`, optional): All candidate options that
            did not win in a round of voting.

    Raises:
        :py:exc:`TypeError`: If all potential outcomes are blank.
    """
    _condtypes = ['winner', 'loser', 'tied']
    def __init__(self, **order):
        for cond in Result._condtypes:
            setattr(self, '_'+cond, order.get(cond, []))
        
        # Check and correct conditions states, if possible
        self._resolve_incorrect_states_on_init()
    
    @property  
    def winner(self):
        return self._winner

    @property  
    def loser(self):
        return self._loser

    @property  
    def tied(self):
        return self._tied
    
    @classmethod
    def ord_items(cls, x, y):
        """Creates new :class:`Result` from vote counts between two candidates.
        
        Attributes:
            x (:obj:`tuple` of :obj:`str`, :obj:`int`): First entry is 
                candidate label and the second is number of votes for said 
                candidate.
            y (:obj:`tuple` of :obj:`str`, :obj:`int`): First entry is 
                candidate label and the second is number of votes for said 
                candidate.
        
        Returns:
            :class:`Result` with correct outcome between the two candidates.
        """
        if x[1] > y[1]:
            return (cls(winner=x[0],loser=y[0]), x[1])
        elif x[1] < y[1]:
            return (cls(winner=y[0], loser=x[0]), y[1])
        else:
            return (cls(tied=[x[0], y[0]]), x[1])
    
    @staticmethod
    def _cmp_type(r, ty):
        return set(listize(getattr(r, ty)))
    
    def _resolve_incorrect_states_on_init(self):
        """Checks for, and resolves incongruent condition states, if possible
        
        If winner and tied conditions are blank, and loser is not, loser
        entries are moved to tied and loser made blank (while it's possible to
        see such a condition as all candidates tied for winning or losing, the
        developers of the project would prefer a consistent outcome).
        
        If the user has passed a list of winners to the Result constructor, the
        winner entries are moved to tied (if not already present there). The
        winner field is then blanked, 
        
        Raises:
            :py:exc:`TypeError`: If all potential outcomes are blank.
        """
        if (self.winner == []) and (self.tied == []):
            if self.loser == []:
                raise TypeError("Null result object is not permissible.")
            self._tied = self._loser
            self._loser = []
            return
        
        if type(self.winner) is list:
            if type(self.tied) is list:
                self._tied = list(self._tied)
            
            if len(self.winner) > 0:
                for winner in self.winner:
                    if winner not in self.tied:
                        self._tied.append(winner)
            self._winner = []
             
    
    def __eq__(self, other):
        for ty in Result._condtypes:
            if not Result._cmp_type(self, ty) == Result._cmp_type(other, ty):
                return False
        return True          
    
    def __repr__(self):
        if self._tied:
            return "<Result(tied={0}), loser={1}>".format(self._tied,
                                                          self._loser)
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
        winner, loser = (res.tied, []) if res.tied else (res.winner, res.loser)
        for itm in desclist[2:]:
            if itm[1] > bar:
                loser = safe_list_append(winner, loser)
                winner = itm[0]
                bar = itm[1]
            elif itm[1] < bar:
                loser = safe_list_append(itm[0], loser)
            else:
                winner = safe_list_append(winner, itm[0])
        
        res = Result(winner=winner, loser=loser)
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
    def __init__(self, choices, score_range=(0,10)):
        self._choices = choices
        self.score_range_min = score_range[0]
        self.score_range_max = score_range[1]
        
        self._check_ranges() 
        
    @property    
    def choices(self):
        return self._choices
    
    def get_scores(self):
        return self.choices.items()
    
    def _check_ranges(self):
        if self.score_range_min >= self.score_range_max:
            raise TypeError("Minimum value must be LESS THAN maximum value.")
        for choice, score in self._choices.items():
            if score > self.score_range_max or score < self.score_range_min:
                msg = "{0} falls outside of range [{1}, {2}] for candidate {3}"
                raise VotingError(
                    msg.format(
                        score, 
                        self.score_range_min, 
                        self.score_range_max,
                        choice
                    )
                )
        return
