from django import forms

from .models import Exercise, Dates

import datetime as DT
import distances.helpers.sports as spo

from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
			Submit, Layout, Fieldset, ButtonHolder, 
			Div, HTML, Field
			)
class DateInput(forms.DateInput):
	input_type = 'date'
	#class = 'datepicker'
	
class ExerciseForm(forms.ModelForm):
	
	def __init__(self, *args, **kwargs):
		super(ExerciseForm, self).__init__(*args, **kwargs)
		
		self.helper = FormHelper(self)
		self.helper.label_class = 'col-sm-2'
		self.helper.field_class = 'col-sm-10'
		self.fields['sub_sport'].required = False
		self.fields['text'].required = False
		self.helper.layout = Layout(
			Div(
				   Div(Fieldset('','sport', 'sub_sport', 'date'), css_class='col-md-4',),
				   Div(Fieldset('Time', 'hours', 'minutes' ), css_class='col-md-2',),
				   Div(Fieldset('Distance', 'distance'), css_class='col-md-2',),
				   #Div('hours', 'minutes',label='Time', css_class='col-md-2', ),
				   #Div('sport', 'hours',  'date', css_class='col-md-2',),
				   #Div('sub_sport', 'minutes', css_class='col-md-2', ),
				   #Div('distance', css_class='col-md-2',),
				   
				   #Div('endDate', css_class='col-md-2',),
				   css_class='row'
				),
			Field('text', rows="3", css_class='input-xlarge'),
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
		fields = [ 'sport', 'sub_sport', 'hours', 'minutes','distance', 'date', 'text']
		labels = {'sport': 'Sport', 'sub_sport': 'Sub sport', 'hours': 'hours', 'minutes': 'minutes',   
		          'distance': 'kilometers', 'date': 'date', 'text': 'description'}
		
		widgets = {
		    #'date': DateInput(),
		    #'date': forms.DateInput(format=('%d-%m-%Y'),attrs={'class': 'datepicker'}),
		    'date': forms.DateInput(attrs={'class': 'datepicker'}),
		    'text': forms.Textarea(attrs={'cols': 80}),
		}
		#widgets = {
		#    'date': forms.TextInput(attrs={'type': 'date'}),
		#    'text': forms.Textarea(attrs={'cols': 80}),
		#}
		
		
		          


class SportForm(forms.Form):
	#CHOICES = (('all', 'All'), ('Running', 'Running'),('Skiing', 'Skiing'),('Cycling', 'Cycling'),)
	alla = ('all', 'All')
	CHOICES = (alla,) + spo.SPORTS_CHOICES
	#field = forms.ChoiceField(choices=CHOICES)
	field = forms.ChoiceField(choices=CHOICES,  
	      widget=forms.Select(attrs={'onchange': 'SportForm.submit();'}))
	#field = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

class DateForm(forms.ModelForm):
	class Meta:
		model = Dates
		fields = ['startDate', 'endDate']
		labels = {'startDate': 'Start Date', 'endDate': 'End Date'}
		widgets = {
		    'startDate': DateInput(),
		    'endDate': DateInput(),
		}
	
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
			HTML('<a  class="btn btn-large btn-info" data-toggle="modal"  data-target="#exerciseModal" > Add New </a>')
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
	#class Meta:
	#	model = Exercise
	#	widgets = {
	#	    'startDate': DateInput(),
	#	    'endDate': DateInput(),
	#		}
	#class Meta:
		#model = Exercise
		#fields = ['startDate', 'endDate', 'sport']
		#labels = {'startDate': 'Start Date', 'endDate': 'End Date', 'sport': 'Sport'}
		#widgets = {
		    #'startDate': DateInput(),
		    #'endDate': DateInput(),
		#}


    
