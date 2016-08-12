'''
Created on Aug 8, 2016

@author: Thomas Adriaan Hellinger
'''
from flask import Blueprint, render_template, jsonify

from simulations.borda_scoring_demo import BordaScoringDemo
from simulations.random_condorcet_demo import RandomCondorcetDemo
from web.simulations.forms import RandomCondorcetForm, BordaScoringForm


blueprint = Blueprint("scenarios", __name__, url_prefix='/scenarios',
                      static_folder="web/static/",
                       static_url_path="/web/static")
from flask.views import MethodView


class ScenarioMainView(MethodView):
    def get(self):
        scenarios = {
         'Borda Scoring Demo' : 'borda_scoring',
         'Random Condorcet Demo': 'random_condorcet'
        }
        return render_template('scenarios.html', scenarios=scenarios.items())



class BordaScoringView(MethodView):
    def __init__(self):
        class BordaScoringInitialForm():
            irrelevant_candidate_a = "Jill Stein"
            irrelevant_candidate_b = "Gary Johnson"
            irrelevant_color = "gray"
            preferred_candidate_a = "Hillary Clinton"
            preferred_candidate_b = "Donald Trump"
            strategic_count_for_a = 10
            strategic_count_for_b = 10
            preferred_color_a = "blue"
            preferred_color_b = "red"
            seed_field = 10
            submit_run = False  
        self.form = BordaScoringForm(obj=BordaScoringInitialForm)
        self.form.populate_obj(BordaScoringInitialForm())
    
    def get(self):
        return render_template('borda_scoring.html', form=self.form)

    def post(self):
        if self.form.validate():
            bsd = BordaScoringDemo(
                [self.form.preferred_candidate_a.data,
                 self.form.preferred_candidate_b.data],
                [self.form.irrelevant_candidate_a.data,
                 self.form.irrelevant_candidate_b.data],                   
                [],
            )
    
class RandomCondorcetView(MethodView):
    def __init__(self):
        class RandomCondorcetInitialForm():
            number_of_voters = 10
            seed_field = 100
            candidates = ['Donald Trump', 'Hillary Clinton', 
                          'Jill Stein', 'Gary Johnson']
            colors = ['red', 'blue', 'green', 'yellow']
            submit_run = False
        self.form = RandomCondorcetForm(obj=RandomCondorcetInitialForm)
        self.form.populate_obj(RandomCondorcetInitialForm())
    
    def get(self):
        return render_template(
            'random_condorcet.html', 
            form=self.form,
            output=None, 
            cand_colors=zip(self.form.candidates, self.form.colors))
    
    def post(self):
        if self.form.validate():
            rc = RandomCondorcetDemo(self.form.candidates.data)
            output = rc.run(self.form.number_of_voters.data,
                            self.form.seed_field.data)
            cand_colors = zip(self.form.candidates.data, self.form.colors.data)
            output['contests'] = RandomCondorcetView.format_round_scores(
                output['round_scores'],
                {k:v for k,v in cand_colors}
            )
            del output['round_scores']
            return render_template('random_condorcet.html', form=None, 
                                   output=output)
        else:
            return render_template('random_condorcet.html', form=self.form,
                                   output=None)

    @staticmethod
    def format_round_scores(round_scores, colors):
        output = []
        for contest_key, contest_result in round_scores.items():
            c1,c2 = contest_key.split(':')
            contest = "<span style='color: {2}'>{0}</span> v.s. "
            contest += "<span style='color: {3}'>{1}</span>"
            contest = contest.format(c1,c2,colors[c1],colors[c2])
        
            msg = "In contest, {0}: <span style='color: {5}'>{1}</span> "
            if contest_result[c1] > contest_result[c2]:
                msg += "has <strong>{2}</strong> votes, "
                msg += "and <span style='color: {6}'>{3}</span> has {4} votes"
            elif contest_result[c1] < contest_result[c2]:
                msg += "has {2} votes, and <span style='color: {6}'>{3}</span> "
                msg += "has <strong>{4}</strong> votes"
            else:
                msg += "has {2} votes, "
                msg += "and <span style='color: {6}'>{3}</span> has {4} votes"
            output.append(msg.format(contest, c1, 
                                                 contest_result[c1], c2, 
                                                 contest_result[c2],colors[c1], 
                                                 colors[c2]))
        return output
        

blueprint.add_url_rule("/", view_func=ScenarioMainView.as_view("main"))

blueprint.add_url_rule('/borda_scoring/', 
                       view_func=BordaScoringView.as_view("borda_scoring"))
blueprint.add_url_rule('/random_condorcet/',
                       view_func=RandomCondorcetView.as_view('random_condorcet'))
