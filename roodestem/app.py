'''
Created on Aug 3, 2016

@author: Thomas Adriaan Hellinger
'''
import os

from flask import Flask, render_template, jsonify, url_for
from simulations.borda_scoring_demo import BordaScoringDemo
from simulations.random_condorcet_demo import RandomCondorcet

app = Flask(__name__, template_folder="web/templates/",
            static_folder="web/static/", static_url_path="/web/static")

@app.route('/')
def index():
    js_url = url_for('static', filename='js/jquery-3.1.0.min.js')
    js_url = "/web" + js_url
    return render_template('index.html')

@app.route('/scenarios')
def scenarios():
    scenarios = {
         'Borda Scoring Demo' : 'borda_scoring',
         'Random Condorcet Demo': 'random_condorcet'
    }
    return render_template('scenarios.html', scenarios=scenarios.items())

@app.route('/scenarios/borda_scoring/')
def borda_scoring_scenario():
    bsd = BordaScoringDemo()
    output = bsd.run()
    return jsonify(output)

@app.route('/scenarios/random_condorcet/')
def random_condorcet_scenario():
    rc = RandomCondorcet()
    output = rc.run()
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)
    