""" Filters for exercise forms """
#Todo these should only apply for single users

startdate = ''
enddate = ''
sport = 'all'

import django_filters
from .models import Exercise
from .forms import DateInput

#import distances.helpers.sports as spo
import distances.json.sports as spo
#from django_fil

class ExerciseFilter(django_filters.FilterSet):
	date = django_filters.DateFilter()
	date__gt = django_filters.DateFilter(label = 'Start date', name='date',
					lookup_expr='gte',
					widget=DateInput())
	date__lt = django_filters.DateFilter(label = 'End date', name='date', 
					lookup_expr='lte',
					widget=DateInput())
	
	startDate = date__gt
	endDate = date__lt
	#startDate = django_filters.DateFilter(
	#			'start'
	
	sport = django_filters.MultipleChoiceFilter(choices=spo.get_sport_choices())
	sub_sport = django_filters.CharFilter(max_length=25)
	#sub_sport = django_filters.ChoiceFilter(choices=spo.getFieldChoices())
	
	class Meta:
		model = Exercise
		fields=('sport', 'sub_sport', 'date', 'startDate', 'endDate')

class RecordFilter(django_filters.FilterSet):
	sport = django_filters.MultipleChoiceFilter(choices=spo.get_sport_choices())
	sub_sport = django_filters.CharFilter(max_length=25)
	#year = django_filters.Choi
	#days = django_filters.NumberFilter(label='Day count', name='days')
	
	class Meta:
		model = Exercise
		fields=('sport', 'sub_sport',)# 'days',)

class GraphFilter(django_filters.FilterSet):
	date = django_filters.DateFilter()
	date__gt = django_filters.DateFilter(label = 'Start date', name='date',
					lookup_expr='gte',
					widget=DateInput())
	date__lt = django_filters.DateFilter(label = 'End date', name='date', 
					lookup_expr='lte',
					widget=DateInput())
	
	startDate = date__gt
	endDate = date__lt
	sport = django_filters.MultipleChoiceFilter(choices=spo.get_sport_choices())
	
	
	class Meta:
		model = Exercise
		fields=('sport', 'startDate', 'endDate')
	#def get_days(self):
	#	return self.days
