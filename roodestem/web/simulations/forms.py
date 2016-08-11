'''
Created on Aug 8, 2016

@author: Thomas Adriaan Hellinger
'''
import sys

from flask_wtf import Form
from wtforms.fields import IntegerField, SubmitField, FieldList, StringField
from wtforms.validators import NumberRange, InputRequired


class RandomCondorcetForm(Form):
    candidates = FieldList(StringField('Candidate'), 'Candidates',
                           min_entries=2, max_entries=100)
    colors = FieldList(StringField('Color'), 'Colors',
                       min_entries=2, max_entries=100)
    number_of_voters = IntegerField(
        'Number of Voters', 
        validators=[InputRequired(),NumberRange(2,10)]
    )
    seed_field = IntegerField(
        "Seed", 
        validators=[NumberRange(-1*sys.maxsize, sys.maxsize)]
    )
    submit_run = SubmitField("Run")
    
#     def __init__(self, choices=['a', 'b', 'c', 'd']):
#         super()
#         