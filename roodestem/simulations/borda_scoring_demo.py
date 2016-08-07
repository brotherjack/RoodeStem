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
    def __init__(self, choices=['a','b','c', 'd']):
        self._choices = choices

    def run(self, rn=10, randomSeed=True):
        output = {
            "choices": self.choices,
            "assertionPass": 0,
            "rounds":[], 
        }
        assertionPass = 0
        for r in range(0, rn):
            curr_round = {
                "round_name": "round_{0}".format(r),
                "seed": "",
                "assertionPass": True,
                "votes": [],
                "fractional_scoring_results": "",
                "standard_scoring_results": ""
            }
            #print("Choices are: {0}".format(self.choices))
            votes = []
            seed = r
            # TODO: Make sure that random seed is not reselected...ever 
            if randomSeed:
                seed = random.randint(0, sys.maxsize)
            curr_round['seed'] = seed
            randselects = [random.randint(0,1) for _ in range(0, 100)]
            for i in range(0, 50): 
                if randselects[i] == 0:
                    votes.append(OrdinalVote(['a', 'b', 'c', 'd']))
                else:
                    votes.append(OrdinalVote(['a', 'c', 'b', 'd']))
            
            for i in range(50, 100):
                if randselects[i] == 0:
                    votes.append(OrdinalVote(['d', 'b', 'c', 'a']))
                else:
                    votes.append(OrdinalVote(['d', 'c', 'b', 'a']))
    
            bc = BordaCount(self.choices,
                            score_fn=BordaCount.fractional_score_function)
            #print("bc is {0}".format(bc))
            curr_round['votes'] = [v.choices for v in votes]
            results = bc.decide(votes)
            msg = "Results with fractional scoring fn: {0}\nScores: {1}"
            curr_round['fractional_scoring_results'] = msg.format(results, bc.scores)
            #print(msg.format(results, bc.scores))

            bc = BordaCount(self.choices)
            #print("bc is {0}".format(bc))
            results2 = bc.decide(votes)
            msg = "Results with standard scoring fn: {0}\nScores: {1}"
            #print(msg.format(results2, bc.scores))
            curr_round['standard_scoring_results'] = msg.format(results2, bc.scores)
            
            try:
                if results.tied:
                    assert('a' in results.tied and 'd' in results.tied)
                else:
                    assert('a' in results.winner or 'd' in results.winner)
                assert('b' in results.loser and 'c' in results.loser)
            except AssertionError as ae:
                print(ae.message)
                curr_round['assertionPass'] = False
            else:
                assertionPass += 1
            output['rounds'].append(curr_round)
        output['assertionPass'] = assertionPass
        return output
        #print("Assertion passed on {0} runs...".format(assertionPass))
            
    @property
    def description(self):
        return cls.description()
    
    @property
    def choices(self):
        return self._choices
    
    @choices.setter
    def choices(self, choices):
        self._choices = choices
    
    def __repr__(self):
        return "<BordaScoringDemo: choices={0}>".format(self.choices)