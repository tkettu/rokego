from django.db import models
from . fields import IntegerRangeField as irf
from django.contrib.auth.models import User

from datetime import datetime, timedelta
import distances.helpers.sports as spo

#from django.utils import timezone

class Exercise(models.Model):
	"""Single exercise for user"""
	#SKIING = 'Skiing'
	#RUNNING = 'Running'
	#CYCLING = 'Cycling'
	#SPORT_CHOISES = (
	#    (SKIING, 'Skiing'),
	#    (RUNNING, 'Running'),
	#    (CYCLING, 'Cycling'),
	#)
	
	SPORTS_CHOICES = spo.SPORTS_CHOICES
	
	sport = models.CharField(max_length=20,
	                          choices=SPORTS_CHOICES,
	                          default=SPORTS_CHOICES[0][0]
	)
	
	sub_sport = models.CharField(max_length=25, default='')
	#time = models.TimeField()
	hours = irf(min_value=0, max_value=500, default=0)
	minutes = irf(min_value=0, max_value=59, default=0)
	#seconds = irf(min_value=0, max_value=59, default=0)
	
	
	distance = models.DecimalField(max_digits=6, decimal_places=2, default=0)
	date = models.DateField(default=datetime.now)
	
	#days = irf(min_value=1, max_value=1000, default = 10)
	
	owner = models.ForeignKey(User)
	
	text = models.CharField(max_length=300, default='')
	average_speed = 0

	def __str__(self):
		"""Return a string represantion of model."""
		mins = str(self.minutes)
		distanceS = str(self.distance)
		if distanceS[-1] == '0' and distanceS[-2] == '0':
			distanceS = distanceS[0:-3]
		
		if len(mins) <2:
			mins = '0' + mins
		text = (self.sport + ", time: " + str(self.hours) + ":" + mins  
				+ ", distance: " + str(distanceS) + ", date: "+ str(self.date))
		        
		return text
	
	@property
	def time(self):
		mins = str(self.minutes)
		if len(mins) <2:
			mins = ':0' + mins
		else:
			mins = ':' + mins
		return '{0}{1}'.format(self.hours, mins)
	
	@property
	def time_as_hours(self):
		return round(self.hours + self.minutes/60, 2)
	
	@property
	def average_speed(self,speedtype='minkm'):
		""" Returns average speed km/h or min/km"""
		dis = float(self.distance)
		if speedtype=='minkm':
			mins2 = self.hours*60 + self.minutes
			speed = mins2/dis
			mins = int(speed)
			secs = str(int((speed - mins)*60))
			if len(secs) < 2:
				secs = '0' + secs
			
			return '{0}{1}'.format(mins,','+str(secs))
			#minuts = int(self.hours)*60 + int(self.minutes)
			#return round(minuts/dis, 2)
		else:
			hoursD = int(self.hours) + int(self.minutes)/60
			return round(dis/hoursD, 2)
	
	
		

	
def get_time_before(days):
	return datetime.today() - timedelta(days=days)
	
class Dates(models.Model):
	today = datetime.now
	week_ago= get_time_before(days=7) #Does this work always???date
	startDate = models.DateField(default=week_ago)
	endDate = models.DateField(default=today)
	
#Tutorial for django-tables2
class Person(models.Model):
	name = models.CharField(verbose_name="full name", max_length=200)
	tags = models.CharField(max_length=20, default='')
	
	
	#def distance(self):
	#	return str(self.distance)
	
	            
	       
