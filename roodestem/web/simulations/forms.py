'''
Created on Aug 8, 2016

@author: Thomas Adriaan Hellinger
'''
from wtforms.form import Form
from wtforms.fields import IntegerField, SubmitField
from wtforms.validators import NumberRange, DataRequired


class RandomCondorcetForm(Form):
    number_of_voters = IntegerField(
                                    'Number of Voters', 
                                    default=10,
                                    validators=[NumberRange(2,10), 
                                                DataRequired()]
    )
    submit_run = SubmitField("Run")