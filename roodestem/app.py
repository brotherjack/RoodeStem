'''
Created on Aug 3, 2016

@author: Thomas Adriaan Hellinger
'''
import os

from flask import Flask, render_template, jsonify, url_for
from IPython import embed

try:
    from roodestem.simulations.borda_scoring_demo import BordaScoringDemo
    from roodestem.simulations.random_condorcet_demo import RandomCondorcetDemo
    from roodestem.web.simulations.views import blueprint
except ImportError as ie:
    embed()

app = Flask(__name__, template_folder="web/templates/",
            static_folder="web/static/", static_url_path="/web/static")

@app.route('/')
def index():
    return render_template('index.html')

def main():
    app.register_blueprint(blueprint)
    app.secret_key = "bugger this for a game of solders"
    app.run(debug=True)

if __name__ == '__main__':
    main()
    