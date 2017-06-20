from django.db.models import Sum, Avg
#from ..models import Exercise

import distances.filters as filters

class Stats():
	
	def __init__(self):
		"""Init"""
	
	def totals(exercises, phys_quant='distance'):
		"""Shows total (distances) of exercises (object Exercise of models )"""
		tot = exercises.aggregate(Sum(phys_quant))
		return tot[phys_quant+'__sum']
	
	def averages(exercises, phys_quant='distance'):
		tot = exercises.aggregate(Avg(phys_quant))
		return tot[phys_quant+'__avg']
	
	def number_of_exs(exercises):
		return exercises.count()
	
	def totaltime(exercises):
		"""Shows total time of exercises."""
		try:
			hours = Stats.totals(exercises, phys_quant='hours')
			minutes = Stats.totals(exercises, phys_quant='minutes')
			
			timeh = int(hours + (minutes - minutes%60)/60)
			timem = int(minutes%60)
			minstr = str(timem)
			if len(minstr) < 2:
				minstr = '0'+minstr
			return str(timeh) + ':' + minstr
		except TypeError:
			print('Time is none (0) or otherwise non numeric')
		return '0'
	
	def avertime(exercises):
		"""Shows total time of exercises."""
		try:
			hours = Stats.totals(exercises, phys_quant='hours')
			minutes = Stats.totals(exercises, phys_quant='minutes')
			
			timeinminuts = hours*60 + minutes
			aver = timeinminuts/Stats.number_of_exs(exercises)
			minstr = str(int(round(aver%60,0)))
			if len(minstr) < 2:
				minstr = '0'+minstr
			return (str(int(aver/60))+':'+ minstr)
		except TypeError:
			print('Time is none (0) or otherwise non numeric')
		#tot = float(Stats.totaltime(exercises))
		#c = float(Stats.number_of_exs(exercises))
		return '0'
	
	def time_hours(exercises):
		"""Shows total time as hours (h + min/60) of exercises."""
		try:
			hours = Stats.totals(exercises, phys_quant='hours')
			minutes = Stats.totals(exercises, phys_quant='minutes')
			
			timeh = int(hours + (minutes - minutes%60)/60)
			timem = int(minutes%60)
			
			timehours = float(timeh) + float(timem)/60
			return timehours
		except TypeError:
			print('Time is none (0) or otherwise non numeric')
		
		return 0
