'''
Created on Jun 22, 2016

@author: Thomas Adriaan Hellinger
'''
try:
    from .voting_system import (
        CardinalSystem, 
        VotingSystem, 
        CardinalVote, 
        VotingError,
        Result
    )
except SystemError:
    from voting_system import (
        CardinalSystem, 
        VotingSystem, 
        CardinalVote, 
        VotingError,
        Result
    )

class RankedBallot(CardinalSystem):
    def __init__(self, choices, score_range):
        super().__init__(choices)
        self._choices = choices
        self.min_score = score_range[0]
        self.max_score = score_range[1]

        self._check_score_range()
        self.scores = {k:0 for k in self.choices}
        
    @property
    def choices(self):
        return self._choices
    
    def _check_score_range(self):
        if self.min_score >= self.max_score:
            raise TypeError("Minimum value must be LESS THAN maximum value.")
    
    def reset_scores(self):
        self.scores = {k:0 for k in self.choices}
    
    def decide(self, votes, reset_scores=True):
        if reset_scores: 
            self.reset_scores()
        self.tally_votes(votes)
        return self._return_results(self.scores)
    
    def tally_votes(self, votes):
        for vote in votes:
            for cand, score in vote.get_scores():
                if cand not in self.choices or score < self.min_score\
                or score > self.max_score:
                    msg = "Cardinal vote: {0} not in legal parameters of "
                    msg += "ranked vote of candidates {1} in range ({2}, {3})"
                    self.reset_scores()
                    raise VotingError(
                        msg.format(vote, self.choices, 
                                   self.min_score, self.max_score)
                    )
                else:
                    self.scores[cand] += score
    
    def __repr__(self):
        msg = "<RankedBallot: choices={0}, score_range=({1}, {2})>"
        return msg.format(self.choices, self.min_score, self.max_score)
