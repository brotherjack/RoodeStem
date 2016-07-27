'''
Created on Jun 15, 2016

@author: Thomas Adriaan Hellinger
'''
try:
    from .voting_system import (
        CardinalSystem, 
        VotingSystem, 
        OrdinalVote, 
        VotingException,
        Result
    )
except SystemError:
    from voting_system import (
        CardinalSystem, 
        VotingSystem, 
        OrdinalVote, 
        VotingException,
        Result
    )

class BordaCount(CardinalSystem):
    @staticmethod
    def standard_score_function(vote):
        for i in range(1, len(vote)):
            yield  len(vote) - i

    @staticmethod
    def fractional_score_function(vote):
        for i in range(1, len(vote)+1):
            yield 1 / i

    def __init__(self, choices, score_fn=None):
        super().__init__(choices)
        self._choices = choices
        self.scores = {k:0 for k in self.choices}
        if not score_fn:
            self.score_fn = BordaCount.standard_score_function
        else:
            self.score_fn = score_fn

    @property
    def choices(self):
        return self._choices    
        
    def decide(self, votes, reset_scores=True):
        if list(filter(lambda x: x > 0, self.scores.values())) and reset_scores:
            self.scores = {k:0 for k in self.scores.keys()}
        for vote in votes:
            for cand, score in zip(vote, self.score_fn(vote)):
                self.scores[cand] += score
        return self._return_results(self.scores)
    
    def __repr__(self):
        return "<BordaScore: choices={0}>".format(self.choices)
