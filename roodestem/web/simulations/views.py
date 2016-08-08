'''
Created on Aug 8, 2016

@author: Thomas Adriaan Hellinger
'''
from flask import Blueprint, render_template, jsonify

from simulations.borda_scoring_demo import BordaScoringDemo
from simulations.random_condorcet_demo import RandomCondorcetDemo
from web.simulations.forms import RandomCondorcetForm


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
    def get(self):
        bsd = BordaScoringDemo()
        output = bsd.run()
        return jsonify(output)


class RandomCondorcetView(MethodView):
    def __init__(self):
        self.form = RandomCondorcetForm()
    
    def get(self):
        return render_template('random_condorcet.html', form=self.form,
                                   output=None)
    
    def post(self):
        if self.form.validate():
            rc = RandomCondorcetDemo()
            output = rc.run(self.form.number_of_voters.data)
            return render_template('random_condorcet.html', form=None, 
                                   output=output)
        else:
            return render_template('random_condorcet.html', form=self.form,
                                   output=None)


blueprint.add_url_rule("/", view_func=ScenarioMainView.as_view("main"))

blueprint.add_url_rule('/borda_scoring/', 
                       view_func=BordaScoringView.as_view("borda_scoring"))
blueprint.add_url_rule('/random_condorcet/',
                       view_func=RandomCondorcetView.as_view('random_condorcet'))
