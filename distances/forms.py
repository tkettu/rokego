from django import forms

from .models import Exercise#, Dates

import datetime as DT
#import distances.helpers.sports as spo
import distances.json.sports as spo

from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
			Submit, Layout, Fieldset, ButtonHolder, 
			Div, HTML, Field
			)

#import json
#from collections import OrderedDict



class DateInput(forms.DateInput):
	input_type = 'date'
	#class = 'datepicker'



#sport_choises = 'distances/json/sports.json'
owndefault = "Running"

exercise_layout = Layout(
			Div(
				   #Div(Fieldset('','sport', 'sub_sport', 'date'), css_class='col-md-4',),
				   Div(Fieldset('','sport', 'sub_sport', 'date'), css_class='col-md-2'),
				   #Div(Fieldset('Time', 'hours', 'minutes' ), css_class='col-md-2',),
				   Div(Fieldset('', Div('hours', css_class='col-md-1'),
					   Div('minutes', css_class='col-md-1'),
					  css_class='row-fluid',),
					  ),
				   Div(Fieldset('', 'distance'), css_class='col-md-1',),
				   #Div(Field('distance'), css_class='col-md-2',),
				   #Div('hours', 'minutes',label='Time', css_class='col-md-2', ),
				   #Div('sport', 'hours',  'date', css_class='col-md-2',),
				   #Div('sub_sport', 'minutes', css_class='col-md-2', ),
				   #Div('distance', css_class='col-md-2',),
				   
				   #Div('endDate', css_class='col-md-2',),
				   css_class='row'
				   #css_class='container'
				),
			Field('text', rows="3", css_class='input-xlarge'),
			)
#def getChoices():
	#with open(sport_choises) as f:
		#data = json.load(f, object_pairs_hook=OrderedDict)
		#choices = []
		#for d in data:
			#choices.append((d, d))
	#return tuple(choices)
	
#def getFieldChoices(key_field='Running'):
	#with open(sport_choises) as f:
		#json_data = json.load(f)
		#choices = []
		#if key_field  in json_data:
			#subfields = json_data[key_field]
			#for field in subfields:
				#choices.append((field, field))
	#return tuple(choices) 
	##return d
	

class ExerciseForm(forms.ModelForm):
	
	def __init__(self, *args, **kwargs):
		#self._key_field = kwargs.pop('sport', None)
		#self._key_field = kwargs.pop('sport', 'Running')
		super(ExerciseForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		self.fields['sport'] = forms.ChoiceField(
			choices = spo.get_sport_choices(),
			initial = owndefault,
			widget = forms.Select(attrs={			
					#"onChange":"getSubSports(value)"
					"onChange":"getSubSports()"
					})
		)
		self.fields['sub_sport'] = forms.CharField(
			#https://djangosteps.wordpress.com/2012/01/12/filtered-menus-in-django/
			label = 'Type',
			required = False,
			initial = '',
			widget = forms.Select()
		)
		self.fields['sub_sport'].widget.choices = spo.getFieldChoices(owndefault)
		
		self.helper.label_class = 'col-sm-2'
		self.helper.field_class = 'col-sm-10'
		#self.fields['sub_sport'].required = False
		self.fields['text'].required = False
		self.helper.layout = Layout(
			exercise_layout,
		
			ButtonHolder(
				Submit('submit','Submit'),
				Submit('submitother', 'Save and add other')
				),
				#css_class='row'
				#), #/Div
			)
			
		
	class Meta:
		model = Exercise
		#fields = []
		fields = [ 'sport', 'sub_sport', 'hours', 'minutes', 'distance', 'date', 'text']
		labels = {'sport': 'Sport', 'sub_sport': 'Type', 'hours': 'Hours', 'minutes': 'Minutes',   
		          'distance': 'Kilometers', 'date': 'Date', 'text': 'Description'}
		
		widgets = {
		    'date': forms.DateInput(attrs={'class': 'datepicker'}),
		    'text': forms.Textarea(attrs={'cols': 80}),
		}
		
		
class EditExerciseForm(ExerciseForm):
	def __init__(self, *args, **kwargs):
		super(EditExerciseForm, self).__init__(*args, **kwargs)
		#self.helper = FormHelper(self)
		self.helper.layout = Layout(
			exercise_layout,
			ButtonHolder(
				Submit('submit','Save changes'),
				HTML('<button name="delete" class="btn btn-warning pull-right" \
						value="remove" >Delete</button>')
			),
		)


#class SportForm(forms.Form):
	##CHOICES = (('all', 'All'), ('Running', 'Running'),('Skiing', 'Skiing'),('Cycling', 'Cycling'),)
	#alla = ('all', 'All')
	#CHOICES = (alla,) + spo.SPORTS_CHOICES
	##field = forms.ChoiceField(choices=CHOICES)
	#field = forms.ChoiceField(choices=CHOICES,  
	      #widget=forms.Select(attrs={'onchange': 'SportForm.submit();'}))
	
	
class ExerciseFilterFormHelper(FormHelper):
	form_method = 'GET'
	layout = Layout(
		
		Fieldset(
			'',
   		    #'Filters',
		    #'sport',
			Div(
				Div('sport', css_class='col-md-2',),
				Div('sub_sport', css_class='col-md-2',),
				Div('startDate', 'endDate', css_class='col-md-2', ),
				#Div('endDate', css_class='col-md-2',),
				css_class='row'
				#css_class='form-group'
			),
		),
		
		ButtonHolder(
			Submit('submit', 'Apply'),
			#HTML('<a  class="btn btn-large btn-info" href="{% url \'distances:new_exercise\' %}"> Add New </a>')
			#HTML('<a  class="btn btn-large btn-info" data-toggle="modal"  \
			#	data-target="#exerciseModal" > Add New </a>'),
			#HTML('{% csrf_token %} <button name="delete" class="btn btn-warning pull-right" \
			#	value="Delete items" formmethod="post">Delete selected</button>')
			),
			
		)
		
	# Todo, not working??
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
				Div('sport', css_class='col-md-2',),
				Div('sub_sport', css_class='col-md-2',),
				#Div('days', css_class='col-md-2',),
				css_class='row'
			),
		),
		
		ButtonHolder(
			Submit('submit', 'Apply')
			)
		)
