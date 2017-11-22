from django import forms

from .models import Exercise  # , Dates

import distances.json.sports as spo

from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Submit, Layout, Fieldset, ButtonHolder,
    Div, HTML, Field
)

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class DateInput(forms.DateInput):
    input_type = 'date'


owndefault = "Running"

# ToDo form format
# SPORT     hours minutes
# TYPE      distance
# Date
# -----Description -----

# And when shrink
# SPORT
# TYPE
# DATE
# HH MM
# Distance
# Description

exercise_layout = Layout(
    Div(
        # Div(Fieldset('','sport', 'sub_sport', 'date'), css_class='col-md-4',),
        Div(Fieldset('', 'sport', 'sub_sport', 'date'), css_class='col-md-2'),
        #Div(Fieldset('Time', 'hours', 'minutes' ), css_class='col-md-2',),
         Div(Fieldset('', Div('hours', css_class='col-md-1'),
                      Div('minutes', css_class='col-md-1'),
                      css_class='row-fluid', ),
             ),

        # Field('hours',placeholder='HH'),Field('minutes', placeholder='MM'),
        Div(Fieldset('', 'distance'), css_class='col-md-1', ),

        css_class='row'

    ),
    Field('text', rows="3", css_class='input-xlarge'),
)


class ExerciseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # self._key_field = kwargs.pop('sport', None)
        # self._key_field = kwargs.pop('sport', 'Running')
        super(ExerciseForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields['sport'] = forms.ChoiceField(
            choices=spo.get_sport_choices(),
            initial=owndefault,
            widget=forms.Select(attrs={
                # "onChange":"getSubSports(value)"
                "onChange": "getSubSports()"
            })
        )
        self.fields['sub_sport'] = forms.CharField(
            label='Type',
            required=False,
            initial='',
            widget=forms.Select()
        )
        self.fields['sub_sport'].widget.choices = spo.getFieldChoices(owndefault)
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-10'
        # self.fields['sub_sport'].required = False
        self.fields['text'].required = False
        self.fields['hours'].required = False
        self.fields['minutes'].required = False
        self.fields['distance'].required = False
        self.helper.layout = Layout(
            exercise_layout,

            ButtonHolder(
                Submit('submit', 'Submit'),
                Submit('submitother', 'Save and add other')
            ),
            # css_class='row'
            # ), #/Div
        )

    class Meta:
        model = Exercise
        # fields = []
        fields = ['sport', 'sub_sport', 'hours', 'minutes', 'distance', 'date', 'text']
        labels = {'sport': 'Sport', 'sub_sport': 'Type', 'hours': 'Hours', 'minutes': 'Minutes',
                  'distance': 'Kilometers', 'date': 'Date', 'text': 'Description'}

        widgets = {
            'date': forms.DateInput(attrs={'class': 'datepicker'}),
            'text': forms.Textarea(attrs={'cols': 80}),
            'hours': forms.NumberInput(attrs={'placeholder': 0}),
            'minutes': forms.NumberInput(attrs={'placeholder': 0}),
            'distance': forms.NumberInput(attrs={'placeholder': 0}),
        }


class EditExerciseForm(ExerciseForm):
    def __init__(self, sport="", sub_sport="", *args, **kwargs):
        # def __init__(self, *args, **kwargs):
        super(EditExerciseForm, self).__init__(*args, **kwargs)
        # self.helper = FormHelper(self)
        self.ownsport = sport

        self.fields['sub_sport'].widget.choices = spo.getFieldChoices(self.ownsport)
        # self.fields['sub_sport'].widget.choices = spo.getFieldChoices(self._key_field)
        self.helper.layout = Layout(
            exercise_layout,
            ButtonHolder(
                Submit('submit', 'Save changes'),
                HTML('<button name="delete" class="btn btn-warning pull-right" \
						value="remove" >Delete</button>')
            ),
        )


class ExerciseFilterFormHelper(FormHelper):
    form_method = 'GET'
    layout = Layout(

        Fieldset(
            '',
            # 'Filters',
            # 'sport',
            Div(
                Div('sport', css_class='col-md-2', ),
                Div('sub_sport', css_class='col-md-2', ),
                Div('startDate', 'endDate', css_class='col-md-2', ),
                # Div('endDate', css_class='col-md-2',),
                css_class='row'
                # css_class='form-group'
            ),
        ),

        ButtonHolder(
            Submit('submit', 'Apply'),

        ),

    )

    class Meta:
        widgets = {
            'startDate': forms.DateInput(attrs={'class': 'datepicker'}),
            'endDate': forms.DateInput(attrs={'class': 'datepicker'}),
        }


class RecordFilterFormHelper(FormHelper):
    form_method = 'GET'
    layout = Layout(
        Fieldset(
            '',
            Div(
                Div('sport', css_class='col-md-2', ),
                Div('sub_sport', css_class='col-md-2', ),
                Div('year', css_class='col-md-2', ),
                # Div('days', css_class='col-md-2',),
                css_class='row'
            ),
        ),

        ButtonHolder(
            Submit('submit', 'Apply')
        )
    )


class GraphFilterFormHelper(FormHelper):
    # graphchoices = ['scatter', 'cumsum']

    form_method = 'GET'
    layout = Layout(
        Fieldset(
            '',
            Div(
                Div('sport', css_class='col-md-2', ),
                Div('startDate', 'endDate', css_class='col-md-2', ),
                css_class='row'
            ),
        ),
        HTML('<label for="id_graphtype" class="control-label ">\
                Graph type\
            </label><br/>'
             '<select value="Graph" name="graphType" id="id_graphtype">\
				<option value="e"></option>\
				<option value="s">Scatter</option>\
				<option value="c">Cumulative sum</option>\
				<option value="b">Box plot</option>\
			  </select>'
             ),

        ButtonHolder(
            Submit('submit', 'Apply')
        )
    )

    class Meta:
        widgets = {
            'startDate': forms.DateInput(attrs={'class': 'datepicker'}),
            'endDate': forms.DateInput(attrs={'class': 'datepicker'}),
        }
