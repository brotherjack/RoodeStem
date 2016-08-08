'''
Created on Aug 8, 2016

@author: Thomas Adriaan Hellinger
'''
from flask_wtf import Form
from wtforms.fields import IntegerField, SubmitField
from wtforms.validators import NumberRange, InputRequired


class RandomCondorcetForm(Form):
    number_of_voters = IntegerField(
                                    'Number of Voters', 
                                    validators=[InputRequired(),NumberRange(2,10)]
    )
    submit_run = SubmitField("Run")