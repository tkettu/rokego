from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.views.generic import TemplateView
from django_tables2 import RequestConfig, SingleTableView

from django.db.models import Sum

from django_filters.views import FilterView


from .models import Exercise, Person
from .forms import (
					ExerciseForm, SportForm, DateForm, 
					ExerciseFilterFormHelper, RecordFilterFormHelper, 
					ExampleForm
					)
from .tables import PersonTable, ExerciseTable
from distances.filters import ExerciseFilter, RecordFilter

from distances.helpers.stats import Stats
import distances.filters as filters


import distances.helpers.records as rec
import distances.helpers.sports as spo

from datetime import datetime, date


import logging

#import pdb; pdb.set_trace()

logger = logging.getLogger(__name__)

exername = 'all'
enddate = ''
startdate = ''

def index(request):
	"""The home page for Distance Tracker."""
	
	if request.user.is_authenticated():
		today = date.today()
		cur_week = today.isocalendar()[1]
		cur_month = today.month
		exercises = Exercise.objects.filter(owner=request.user, 
							date__week=cur_week).all().order_by('-date')
		
		exercises_m = Exercise.objects.filter(owner=request.user, 
							date__month=cur_month).all().order_by('-date')
		
		exes10 = Exercise.objects.filter(owner=request.user).all().order_by('-date')[:10]
		tot = Stats.totals(exercises)
		tottime = Stats.totaltime(exercises)
		
		tot_m =  Stats.totals(exercises_m)
		tottime_m = Stats.totaltime(exercises_m)
		
		
		context = {'dist': tot, 'time' : tottime, 'distm': tot_m, 'timem': tottime_m, 'exercises': exes10}
		
	else:
		context = {'link':'https://www.youtube.com/watch?v=tENiCpaIk9A'}
	
	return render(request, 'distances/index.html', context)
	
@login_required
def exercises(request):
	context = {}
	exercises = Exercise.objects.filter(owner=request.user).all().order_by('-date')
	
	filter = ExerciseFilter(request.GET, queryset = exercises)
	filter.form.helper = ExerciseFilterFormHelper()
	filteredExercises = filter.qs
	
	table = ExerciseTable(filteredExercises)
	
	# set totals, averages etc. table.set...(Stats.get...)
	RequestConfig(request).configure(table)
	context['filter'] = filter
	context['table'] = table
	response = render(request, 'distances/exercises.html', context)
	return response

def example_form(request):
	""" """
	
@login_required	
def new_exercise(request):
	"""Add a new exercise."""

	if request.method != 'POST':
		form = ExerciseForm()
		
	else:
		form = ExerciseForm(data=request.POST)
		
		if form.is_valid():
			new_exercise = form.save(commit=False)
			new_exercise.owner = request.user
			new_exercise.save()
			
			logger.warning(request.POST)
			#if request.POST.get("addone", "submit"):
			if request.POST.get("submit"):
				logger.warning('Going back to exercises?')
				return HttpResponseRedirect(reverse('distances:exercises'))
			elif request.POST.get("submitother"):
				# Inform somehow that new was added
				logger.warning('Going to new_exercises?')
				msg = 'Added ' + str(new_exercise.sport) +  ' ' + str(new_exercise.distance) + ' km.'
				messages.info(request, msg)
				return HttpResponseRedirect(reverse('distances:new_exercise'))
		
	context = {'form': form}
	return render(request, 'distances/new_exercise.html', context)


@login_required
def records(request):
	""" Display different records"""
	context = {}
	exercises = Exercise.objects.filter(owner=request.user).all().order_by('-date')
	
	filter = RecordFilter(request.GET, queryset = exercises)
	filter.form.helper = RecordFilterFormHelper()
		
	sc = spo.SPORTS_CHOICES
	ddays = [7,30,365]#, filter.get_days()]
	
	recs = []
	
	for d in ddays:
		re0 = rec.longest_period(filter.qs, days=d)
		recs.append(re0)
	
	weeks = rec.week_results(filter.qs)
	#recs = rec.longest_period(request.user, days=7, sport='Running')
	context['filter'] = filter
	context['recs'] = recs
	context['weeks'] = weeks
	context['months'] = rec.month_results(filter.qs)
	#context['month'] = months
	
	#context = {'form': form, 'recs': recs, 'weeks': weeks, 'ename': sport}
	return render(request, 'distances/records.html', context)
	
#class ExerciseTableView(TemplateView):
	
	#template_name = 'distances/exercises.html'
	##@login_required
	#def __init__(self, request):
		#self.request = request
	
	##@login_required
	#def get_queryset(self, **kwargs):
		##return Exercise.objects.filter(owner=self.request.user).all()
		#return Exercise.objects.all()
	##@login_required
	
	#def get_context_data(self, **kwargs):
		##context = super(ExerciseTableView, self).get_context_data(**kwargs)
		##context = ExerciseTableView.get_context_data(**kwargs)
		#context = {}
		#exercises = self.get_queryset(**kwargs)
		##check_exercise_owner(exercises, self.request.user)
		#filter = ExerciseFilter(self.request.GET, queryset=exercises)
		#filter.form.helper = ExerciseFilterFormHelper()
		#table = ExerciseTable(filter.qs)
		#RequestConfig(self.request).configure(table)
		#context['filter'] = filter
		#context['table'] = table
		#response = render(self.request, 'distances/exercises.html', context)
		##response.set_cookie(key='id',value=1)
		#return response
	
	#def check_exercise_owner(self, exercise, user):
	#	if exercise.owner != user:
	#		raise Http404
	#	return True	


#@login_required
#def exercises(request):
	#"""Shows user exrcises."""
	##choosen_exercise = 'all'
	##TODO set filter for what before?
	#if request.method != 'POST':
		#form = SportForm()
		##form_date = DateForm()
		#exercise_name = request.GET.get('sport','')
	#else:
		#form = SportForm(data=request.POST)
		##form_date = DateForm(data=request.POST)
		#if form.is_valid():
			#exercise_name = form.cleaned_data['field']
			#filters.sport = exercise_name
		##if form_date.is_valid():
		##	startDate = form_date.cleaned_data['startDate']
		##	endDate = form_date.cleaned_data['endDate']
		##	logger.warning('sdate ' + str(startDate))
		##	filters.startdate = startDate
		##	filters.enddate = endDate
			
		##return HttpResponseRedirect(reverse('distances:exercises/?' + 'sport=' + exercise_name))
		##return HttpResponseRedirect(reverse('distances:exercises2', kwargs={'sport': exercise_name}))
		##return render_to_response('distances:exercises', {'sport': exercise_name})
		##return HttpResponseRedirect(reverse('distances:exercises'))
			##set_exercise_name(exercise_name)
			##exername = exercise_name
			##return HttpResponseRedirect(reverse('distances:exercise/' + exercise_name))
			##Todo tänne palautus all, running, skiing jne.
			##if exercise_name == 'all':
			##	return HttpResponseRedirect(reverse('distances:exercises'))
			##else:
			##	return exercise(request, exercise_name)
			##return HttpResponseRedirect(reverse('distances:exercise/' + exercise_name + '/'))
	
	##setfilter
	##checkFilters(exercisename)
	
	#if 'exercise_name' in locals():
		#exername = exercise_name
	##	logger.warning('Exername ' + exername)
	#else:
		##exername = filters.sport
		#exername = 'all'
	
	##Check if page already loaded and enddate (startdate) filters submitted
	##if 'endDate' in locals(): 
	##	enddate = endDate
	##	startdate = startDate 
	##else:
		##enddate = filters.enddate
	##	enddate = ''
		##startdate = filters.startdate
	##	startdate = ''
	#enddate=''
	#cur_user = request.user
	##logger.info(exername)
	#if exername == 'all':
		#if enddate == '':
			#exercises = Exercise.objects.filter(owner=cur_user).all().order_by('-date')
		#else:
			#exercises = Exercise.objects.filter(owner=cur_user, 
					#date__lte=enddate, date__gte=startdate).all().order_by('-date')
	#else:
		##exercises = Exercise.objects.filter(owner=cur_user, date__lte=enddate, 
		##        date__gte=startdate, sport=exername).all().order_by('-date')
		#exercises = Exercise.objects.filter(owner=cur_user,  
		         #sport=exername).all().order_by('-date')
	##exercises = Exercise.objects.filter(owner=cur_user).all().order_by('-date')
	##date__lte='date_joka_suurin, date__gte='date_joka pienin'
	#try:
		#total_distance = Stats.totals(exercises, 'distance')
		#total_time = Stats.totaltime(exercises)
		
		#total_count = Stats.number_of_exs(exercises)
		
		#aver_distance = round(Stats.averages(exercises, 'distance'),2)
		#aver_time = Stats.avertime(exercises)
	#except TypeError:
		#total_distance = 'NONE'
		#total_time = 'NONE'
		#total_count = 'NONE'
		#aver_distance = 'NONE'
		#aver_time = 'NONE'
		
	#table = ExerciseTable(exercises)
	#RequestConfig(request).configure(table)
	##return render(request, 'distances/people.html', {'table': table})
	
	#context = {'table': table, 'total': total_distance,
	            #'totaltime': total_time, 'count': total_count,
	            #'average': aver_distance, 'averagetime': aver_time,
	            #'form': form}#, 'form_date': form_date}	
	##context = {'exercises': exercises, 'total': total_distance,
	##            'totaltime': total_time, 'count': total_count,
	##            'average': aver_distance, 'averagetime': aver_time,
	##            'form': form, 'form_date': form_date}
	
	##context = {'exercises': exercises, 'total': Stats.total(cur_user, sport=exername),
	            ##'totaltime': Stats.totaltime(cur_user, sport=exername), 
	            ##'form': form, 'form_date': form_date}
	
	
	##check_topic_owner(exercises, cur_user)
	
	#return render(request, 'distances/exercises.html', context)

@login_required
def edit_exercise(request, exercise_id):
	"""Edit en existing entry"""
	entry = Exercise.objects.get(id=exercise_id)
	#topic = entry.topic
	#if topic.owner != request.user:
	#	raise Http404
	cur_user = request.user
	check_exercise_owner(entry, cur_user)
	if request.method != 'POST':
		# Initial request; pre-fill form from the current entry.
		form = ExerciseForm(instance=entry)
	else:
		# POST data submitted; process data
		if request.POST.get('delete'):
			entry.delete()
			return HttpResponseRedirect(reverse('distances:exercises'))
		
		form = ExerciseForm(instance=entry, data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('distances:exercises'))
	
	context = {'exercise': entry, 'form': form}
	return render(request, 'distances/edit_exercise.html', context)

def get_exercises(names, cur_user):
	exercises = Exercise.objects.filter(owner=cur_user, sport = 'NOSPORT').all().order_by('-date')
	for s in names:
		ex = Exercise.objects.filter(owner=cur_user, sport = s).all().order_by('-date')
		exercises = exercises | ex
	
	return exercises
	


def set_exercise_name(name):
	exername = name

def get_exercise_name():
	return exername

@login_required	
#def exercise(request, exercisename):
def exercise(request, exercisename):
	"""Show single sport and its totals."""
		
	e = exercisename
	cur_user = request.user
	exercises = Exercise.objects.filter(owner=cur_user, sport=e).order_by('-date')
	context = {'exercises': exercises, 'total': Stats.total(cur_user, sport=e),
	            'totaltime': Stats.totaltime(cur_user, sport=e)}
	return render(request, 'distances/exercises.html', context)



def get_sport_form(request):
	"""gets sport from sport form"""
	if request.method != 'POST':
		form = SportForm()
	else:
		form = SportForm(data=request.POST)
		if form.is_valid():
			exercise_name = form.cleaned_data['field']
	
	if 'exercise_name' in locals():
		return {'form': form, 'exercise_name': exercise_name}
	else:
		return {'form': form}
		
@login_required
def graphs(request):
	""" Display graphs"""
	
	context = {'graph': 'There is distance-time graph etc.'}
	return render(request, 'distances/graphs.html', context)	

def check_exercise_owner(exercise, user):
	if exercise.owner != user:
		raise Http404
	return True	

def get_stats(cur_user, sport='all'):
	""" method for averages total ..."""
	

#Tutorial for django-tables2
def people(request):
	table = PersonTable(Person.objects.all())
	RequestConfig(request).configure(table)
	return render(request, 'distances/people.html', {'table': table})	

#class FilteredPersonListView(FilterView, SingleTableView):
	#table_class = PersonTable
	#model = Person
	#template_name = 'people.html'
	
	#filterset_class = PersonFilter
		
