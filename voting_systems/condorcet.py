from .voting_system import OrdinalSystem, VotingSystem, OrdinalVote, VotingException
from itertools import combinations


class Result:
    def __init__(self, *order):
        if len(order) > 1:
            self._winner = order[0]
            self._loser = order[1]
            self._tied = None
        else:
            self._winner = None
            self._loser = None
            self._tied = order[0]
    
    @property  
    def winner(self):
        return self._winner

    @property  
    def loser(self):
        return self._loser

    @property  
    def tied(self):
        return self._tied

    def __repr__(self):
        if self._tied:
            return "<Result(tied={0})>".format(self._tied)
        else:
            return "<Result(winner={0}, loser={1})>".format(self._winner,
                                                            self._loser)
       

class CondorcetParadox(VotingException):
    def __init__(self, traveled, el):
        cycle = " > ".join(traveled)
        cycle += " > " + el
        self.msg = "Detected cycle: {0}".format(cycle)

class CondorcetMethod(OrdinalSystem):
    def __init__(self, choices):
        super()
        self._choices = choices
        self._order_matrix = {k1:\
            {k2:None if k2 != k1 else 0 for k2 in choices} for k1 in choices}


    @property
    def choices(self):
        return self._choices

    def decide(self, votes, verbose=False):
        ordering = self._run_comparisons(votes, verbose)
        self._make_order_matrix(ordering)
        results = {}
        for k in self._order_matrix.keys():
            results[k] = sum(self._order_matrix[k].values()) 
        return results

    def _run_comparisons(self, votes, verbose):
        round_scores = {}
        ordering = []
        for c1, c2 in combinations(self._choices, 2):
            contest = "{0} v.s. {1}".format(c1,c2)
            round_scores[contest] = {c1:0, c2:0}
            if verbose:
                print(c1," v.s. ",c2)
            for vote in votes:
                c1i = vote.ranking(c1)
                c2i = vote.ranking(c2)
                if c1i < c2i or c2i < c1i:
                    winner = c1 if c1i < c2i else c2
                    loser = c1 if c1i > c2i else c2
                    round_scores[contest][winner] += 1
                    if verbose:
                        msg = "{0} beats {1} in the vote {2}"
                        print(msg.format(winner, loser, vote))
                else:
                    msg = "{0} does not display complete ordering"
                    raise VotingError(msg.format(vote))
            if verbose:
                msg = "In contest, {0}: {1} has {2} votes, "
                msg += "and {3} has {4} votes"
                print(msg.format(contest, c1, round_scores[contest][c1],
                                 c2, round_scores[contest][c2]))
            if round_scores[contest][c1] < round_scores[contest][c2]:
                ordering.append(Result(c2, c1))
            elif round_scores[contest][c2] < round_scores[contest][c1]:
                ordering.append(Result(c1, c2))
            else:
                ordering.append(Result([c1,c2]))
        return ordering  

    def _make_order_matrix(self, orders):
        for order in orders:
            if order.tied:
                self._order_matrix[order.tied[0]][order.tied[1]] = 0
                self._order_matrix[order.tied[1]][order.tied[0]] = 0
            else:
                self._order_matrix[order.winner][order.loser] = 1
                self._order_matrix[order.loser][order.winner] = -1
        return

    def _check_for_condercet_paradox(self):
        i=0
        fk = list(self._order_matrix.keys())[i]
        while 1 not in self._order_matrix[fk].values():
            i += 1
            fk = list(self._order_matrix.keys())[i]
        def follow_path(goto, beento):
            paths = [k for k,v in self._order_matrix[goto].items() if v == 1]
            if not paths:
                return 0
            else:
                if goto in beento:
                    raise CondorcetParadox(beento, goto)
                else:
                    beento.append(goto)
                    return [follow_path(p, beento) for p in paths]
        try:
            return follow_path(fk, [])
        except CondorcetParadox as cp:
            print(cp.msg)

    def __repr__(self):
        return "<CondorcetMethod: choices={0}>".format(self.choices)

if __name__ == '__main__':
    a = 'a'
    b = 'b'
    c = 'c'
    d = 'd'
    e = 'e'

    import random
    choices = [a,b,c,d,e]
    cm = CondorcetMethod(choices)
    votes = [OrdinalVote(random.sample(choices, 5)) for i in range(0, 10)]
    print(cm.decide(votes))


