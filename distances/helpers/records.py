"""records.py - calculate best periods, longest streaks etc """
from ..models import Exercise
from datetime import timedelta, date

import calendar
import collections
from collections import Counter


#def longest_period(user, days=7, sport='all'):
def longest_period(exercises, days=7):
	"""Calculate which period has longest distance """
	#if sport == 'all':
	#	exercises = Exercise.objects.filter(owner=user).order_by('date')
	#else:
	#	exercises = Exercise.objects.filter(owner=user, sport=sport).order_by('date')
	#exercises = get_exercises(user, sport, 'date')
	#totalD = 0
	exercises = exercises.order_by('date')
	finTotal = 0
	m = exercises.count()
	period =['', '']
	totalD = 0
	for i in range(m):
		
		sd = exercises[i].date   #start point
		ed = sd
		totalD = exercises[i].distance
		
		j = i
		while True:
			if j+1 < m: 
				nextEx = exercises[j+1]
				if nextEx.date - sd < timedelta(days=days):
					totalD += nextEx.distance
					ed = nextEx.date
				else:
					break
			else:
				break
			j += 1	
		
		if totalD > finTotal:
			finTotal = totalD
			period[0] = sd
			period[1] = ed
		
		
	retval = { 'days': days, 'distance': finTotal, 
					'startDate': period[0], 'endDate': period[1]}
	
	return retval
		

def week_results(exercises):
	"""return results for different weeks."""
	
	weeks = []
	for e in exercises:
		weekYear = get_week_year(e)
		weeks.append((weekYear,e.distance, e.time_as_hours)) #e.date.year
	
	weektotals = collections.OrderedDict()
	weektime = collections.OrderedDict()
	for k,v1, v2 in weeks:
		weektotals[k] = weektotals.get(k,0) + v1
		weektime[k] = weektime.get(k,0) + v2
		
	tots = [weektotals, weektime]
	tot = collections.OrderedDict()
	for k in weektotals:
		tot[k] = tuple(tot[k] for tot in tots)
	
	return tot
	#return weektotals
		
#def week_time(exercises):
	#"""Return time for weeks."""
	
	#weeks = []
	#for e in exercises:
		#weekYear = get_week_year(e)
		#weeks.append((weekYear,e.time_as_hours)) #e.date.year
	
	#weektotals = collections.OrderedDict()
	#for k,v in weeks:
		#weektotals[k] = weektotals.get(k,0) + v
	
	#return weektotals
	
	

def get_week_year(e):
	weekn = e.date.isocalendar()[1] # week number
	yearn = e.date.isocalendar()[0] # year number
	
	return str(weekn) + '/' + str(yearn)
	
def month_results(exercises):
	"""return results for different months."""
	months = []
	for e in exercises:
		monthn = e.date.month
		yearn = e.date.year
		monthY = str(monthn) + '/' + str(yearn)
		months.append((monthY, e.distance, e.time_as_hours))
	
	monthtotals = collections.OrderedDict()
	monthtime = collections.OrderedDict()
	for k,v,v2 in months:
		monthtotals[k] = monthtotals.get(k,0) + v
		monthtime[k] = monthtime.get(k,0) + v2
	
	tots = [monthtotals, monthtime]
	tot = collections.OrderedDict()
	for k in monthtotals:
		tot[k] = tuple(tot[k] for tot in tots)
	
	return tot
	
	#return monthtotals
	
def get_most_common(exercises, n=3):
	""" Get n most common sports """
	exes = [e.sport for e in exercises]
	cnt = Counter()
	for e in exes:
		cnt[e] +=1
	
	commons = cnt.most_common(n)
	commons_array = [co[0] for co in commons]
	return commons_array
	
def get_exercises(user, sport, order):
	if sport == 'all':
		return Exercise.objects.filter(owner=user).order_by('date')
	else:
		return Exercise.objects.filter(owner=user, sport=sport).order_by('date')
	
