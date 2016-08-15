'''
Created on Aug 8, 2016

@author: Thomas Adriaan Hellinger
'''
from flask_wtf import Form
from wtforms.fields import IntegerField, SubmitField, FieldList, StringField
from wtforms.validators import(
    NumberRange, 
    InputRequired, 
    ValidationError,
    DataRequired
)


class RandomCondorcetForm(Form):
    candidates = FieldList(StringField('Candidate'), 'Candidates',
                           min_entries=2, max_entries=100)
    colors = FieldList(StringField('Color'), 'Colors',
                       min_entries=2, max_entries=100)
    number_of_voters = IntegerField(
        'Number of Voters', 
        validators=[InputRequired(),NumberRange(2,10)]
    )
    seed_field = IntegerField("Seed", validators=[DataRequired()])
    submit_run = SubmitField("Run")


class BordaScoringForm(Form):
    def validate(self):
        if super().validate():
            if self.start_seed_field.data > self.end_seed_field.data:
                self.errors.update({self.start_seed_field.label.field_id:
                                    "Start seed must be less than end seed."})
                return False
            else:
                return True
    
    irrelevant_candidate_a = StringField('Irrelevant Candidate A')
    irrelevant_candidate_b = StringField('Irrelevant Candidate B') 
    irrelevant_color = StringField('Color for Irrelevant Candidate')
    
    preferred_candidate_a = StringField('Preferred Candidate A')
    preferred_candidate_b = StringField('Preferred Candidate B')
    
    strategic_count_for_a = IntegerField("Number of voters for A")
    strategic_count_for_b = IntegerField("Number of voters for B")
    
    preferred_color_a = StringField('Color for preferred Candidate A')
    preferred_color_b = StringField('Color for preferred Candidate B')
    
    start_seed_field = IntegerField("Starting Seed",
                                    validators=[DataRequired()])
    end_seed_field = IntegerField("Ending Seed", validators=[DataRequired()])
    submit_run = SubmitField("Run")