from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.views.generic import TemplateView
from django_tables2 import RequestConfig, SingleTableView

from django.db.models import Sum

from django_filters.views import FilterView


from .models import Exercise
from .forms import (
					ExerciseForm, SportForm, #DateForm, 
					ExerciseFilterFormHelper, RecordFilterFormHelper,
					EditExerciseForm
					)
from .tables import  ExerciseTable
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
		cur_year = today.year
		exercises = Exercise.objects.filter(owner=request.user, 
							date__week=cur_week, date__year=cur_year).all().order_by('-date')
		
		exercises_m = Exercise.objects.filter(owner=request.user, 
							date__month=cur_month, date__year=cur_year).all().order_by('-date')
		
		exes10 = Exercise.objects.filter(owner=request.user).all().order_by('-date')[:10]
		tot = Stats.totals(exercises)
		tottime = Stats.totaltime(exercises)
		
		tot_m =  Stats.totals(exercises_m)
		tottime_m = Stats.totaltime(exercises_m)
		
		ret_url = 'distances:index'
		if request.method != 'POST':
			form = ExerciseForm()
		
		else:
			modaln = new_exercise_modal(request, ret_url)
			if modaln[1]:
				return HttpResponseRedirect(reverse(modaln[2]))
			form = modaln[0]
			
		context = {'dist': tot, 'time' : tottime, 'distm': tot_m, 
			'timem': tottime_m, 'exercises': exes10, 'form': form}
		
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
	
	# Add new exercise with modal
	ret_url = 'distances:exercises'
	if request.method != 'POST':
		
		form = ExerciseForm()
		
	else:
		
		if request.POST.get('delete'):
			# TODO, implement working multi deleta
			#print(request.POST.getlist('checks'))
			items = request.POST.getlist('checks')
	
		modaln = new_exercise_modal(request, ret_url)
		if modaln[1]:
			return HttpResponseRedirect(reverse(modaln[2]))
		form = modaln[0]
	
	
		
	table = ExerciseTable(filteredExercises)
	
	# set totals, averages etc. table.set...(Stats.get...)
	RequestConfig(request).configure(table)
	context['filter'] = filter
	context['table'] = table
	#context['form'] = modalForm
	context['form'] = form
	response = render(request, 'distances/exercises.html', context)
	return response


def new_exercise_modal(request, ret_url):
	form = ExerciseForm(data=request.POST)
	
	isForm = False
	if form.is_valid():
		new_exercise = form.save(commit=False)
		new_exercise.owner = request.user
		new_exercise.save()
		
		
		if request.POST.get("submit"):
			isForm = True
			#return HttpResponseRedirect(reverse(ret_url))
		elif request.POST.get("submitother"):
			msg = 'Added ' + str(new_exercise.sport) +  ' ' + str(new_exercise.distance) + ' km.'
			ret_url = 'distances:new_exercise'
			isForm = True
			#return HttpResponseRedirect(reverse('distances:new_exercise'))
	return [form, isForm, ret_url]
	
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
	
	# Todo optimize longest period
	#for d in ddays:
	#	re0 = rec.longest_period(filter.qs, days=d)
	#	recs.append(re0)
	
	weeks = rec.week_results(filter.qs)
	#recs = rec.longest_period(request.user, days=7, sport='Running')
	context['filter'] = filter
	#context['recs'] = recs
	context['weeks'] = weeks
	context['months'] = rec.month_results(filter.qs)
	#context['month'] = months
	
	#context = {'form': form, 'recs': recs, 'weeks': weeks, 'ename': sport}
	return render(request, 'distances/records.html', context)
	

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
		form = EditExerciseForm(instance=entry)
	else:
		# POST data submitted; process data
		if request.POST.get('delete'):
			entry.delete()
			return HttpResponseRedirect(reverse('distances:exercises'))
		
		form = EditExerciseForm(instance=entry, data=request.POST)
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
	
		
