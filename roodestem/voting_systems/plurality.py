'''
Created on Jul 27, 2016

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


class PluralityBallot(CardinalSystem):
    def __init__(self, choices, can_abstain=True):
        super().__init__(choices)
        self._choices = choices
        self.can_abstain = can_abstain
        
        self.reset_scores()
        
    @property
    def choices(self):
        return self._choices
        
    def decide(self, votes, reset_scores=True):
        if reset_scores:
            self.reset_scores()
        self.tally_votes(votes)
        return self._return_results(self.scores)
    
    def reset_scores(self):
        self.scores = {k:0 for k in self.choices}
    
    def tally_votes(self, votes):
        for vote in votes:
            voted_for = vote.get_scores_equal_to(1)
            if len(voted_for) > 1:
                msg = "May only vote for one candidate under PluralityBallot"
                raise VotingError(msg)
            elif len(voted_for) == 0:
                if self.can_abstain:
                    continue
                else:
                    msg = "No vote detected and abstaining not permitted"
                    raise VotingError(msg)
            else:
                self.scores[voted_for[0]] += 1
    
    def __repr__(self):
        msg = "<PluralityBallot: choices={0}>"
        return msg.format(self.choices)