'''
Created on Jul 6, 2016

@author: Thomas Adriaan Hellinger
'''
import random
import sys

from voting_systems.borda import BordaCount
from voting_systems.voting_system import OrdinalVote
from simulations.scenarios import Scenario


class BordaScoringDemo(Scenario):
    def __init__(self, preferred_candidates, irrelevant_candidates,
                 preferred_colors, irrelevant_color):
        self.preferred_candidates = preferred_candidates
        self.irrelevant_candidates = irrelevant_candidates
        self.preferred_colors = preferred_colors
        self.irrelevant_color = irrelevant_color
        self.choices = self.preferred_candidates + self.irrelevant_candidates 

    def run(self, min_seed, max_seed, strat_a, strat_b):
        output = {
            "choices": self.choices,
            "assertionPass": 0,
            "rounds":[], 
        }
        assertionPass = 0
        for r in range(min_seed, max_seed):
            curr_round = {
                "round_name": "round_{0}".format(r),
                "seed": "",
                "assertionPass": True,
                "fractional_scoring_results": "",
                "standard_scoring_results": ""
            }
            votes = []
            seed = r
            curr_round['seed'] = seed
            random.seed(seed)
            randselects = [
                random.randint(0,1) for _ in range(0, strat_a+strat_b)
            ]
            irr_can1, irr_can2 = self.irrelevant_candidates
            pref_can1, pref_can2 = self.preferred_candidates
            for i in range(0, strat_a): 
                if randselects[i] == 0:
                    votes.append(OrdinalVote([pref_can1, irr_can1, 
                                              irr_can2, pref_can2]))
                else:
                    votes.append(OrdinalVote([pref_can1, irr_can2, 
                                              irr_can1, pref_can2]))
            
            for i in range(strat_a, strat_a+strat_b):
                if randselects[i] == 0:
                    votes.append(OrdinalVote([pref_can2, irr_can1, 
                                              irr_can2, pref_can1]))
                else:
                    votes.append(OrdinalVote([pref_can2, irr_can2, 
                                              irr_can1, pref_can1]))
    
            bc = BordaCount(self.choices,
                            score_fn=BordaCount.fractional_score_function)
            
            results = bc.decide(votes)
            msg = "Results with fractional scoring fn: {0}\nScores: {1}"
            curr_round['fractional_scoring_results'] = msg.format(results, bc.scores)

            bc = BordaCount(self.choices)
            results2 = bc.decide(votes)
            msg = "Results with standard scoring fn: {0}\nScores: {1}"
            curr_round['standard_scoring_results'] = msg.format(results2, bc.scores)
            
            try:
                if results.tied:
                    assert(pref_can1 in results.tied and\
                           pref_can2 in results.tied)
                else:
                    assert(pref_can1 in results.winner or\
                           pref_can2 in results.winner)
                assert(irr_can1 in results.loser and irr_can2 in results.loser)
            except AssertionError as ae:
                curr_round.update({"assertion_fail": ae.message})
                curr_round['assertionPass'] = False
            else:
                assertionPass += 1
            output['rounds'].append(curr_round)
        output['assertionPass'] = assertionPass
        return output
            
    @property
    def description(self):
        return cls.description()
    
    def __repr__(self):
        return "<BordaScoringDemo: choices={0}>".format(self.choices)