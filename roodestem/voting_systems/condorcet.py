try:
    from .voting_system import (
        OrdinalSystem, 
        VotingSystem, 
        OrdinalVote, 
        VotingException,
        Result
    )
except SystemError:
    from voting_system import (
        OrdinalSystem, 
        VotingSystem, 
        OrdinalVote, 
        VotingException,
        Result
    )

from itertools import combinations
       

class CondorcetParadox(VotingException):
    def __init__(self, traveled, el):
        cycle = " > ".join(traveled)
        cycle += " > " + el
        self.msg = "Detected cycle: {0}".format(cycle)

class CondorcetMethod(OrdinalSystem):
    def __init__(self, choices):
        super().__init__(choices)
        self._choices = choices
        self._order_matrix = {k1:\
            {k2:None if k2 != k1 else 0 for k2 in choices} for k1 in choices}


    @property
    def choices(self):
        return self._choices

    def decide(self, votes):
        ordering, round_scores = self._run_comparisons(votes)
        self._make_order_matrix(ordering)
        results = {}
        output = {'results': "", 'round_scores': round_scores}
        for k in self._order_matrix.keys():
            results[k] = sum(self._order_matrix[k].values())
        try: 
            self._check_for_condercet_paradox()
        except CondorcetParadox as cp:
            output['results'] = cp.msg
            return output
        output['results'] = self._return_results(results)
        return output

    def _run_comparisons(self, votes):
        round_scores = {}
        ordering = []
        for c1, c2 in combinations(self._choices, 2):
            contest = "{0}:{1}".format(c1,c2)
            round_scores[contest] = {c1:0, c2:0}
            for vote in votes:
                c1i = vote.ranking(c1)
                c2i = vote.ranking(c2)
                if c1i < c2i or c2i < c1i:
                    winner = c1 if c1i < c2i else c2
                    loser = c1 if c1i > c2i else c2
                    round_scores[contest][winner] += 1
                else:
                    msg = "{0} does not display complete ordering"
                    raise VotingError(msg.format(vote))
            if round_scores[contest][c1] < round_scores[contest][c2]:
                ordering.append(Result(winner=c2, loser=c1))
            elif round_scores[contest][c2] < round_scores[contest][c1]:
                ordering.append(Result(winner=c1, loser=c2))
            else:
                ordering.append(Result(tied=[c1,c2]))
        return ordering, round_scores  

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
        return follow_path(fk, [])

    def __repr__(self):
        return "<CondorcetMethod: choices={0}>".format(self.choices)
