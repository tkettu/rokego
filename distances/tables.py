#tables.py
import django_tables2 as tables
from .models import Person, Exercise

from django.db.models import Sum, Avg

from distances.helpers.stats import Stats

class ExerciseTable(tables.Table):
	time = tables.Column(accessor='time', verbose_name='Time', order_by=('hours', 'minutes'))
	#aver_speed = tables.Column(verbose_name='Average speed')
	aver_speed = tables.Column(accessor='average_speed', verbose_name='Average speed (min/km)',
	                         orderable=False) #Todo orderable??
	edit_entries = tables.TemplateColumn(
			template_code='<a href="{% url \'distances:edit_exercise\' record.id %}">Edit</a>',
			orderable=False
			)
	date = tables.DateColumn(accessor='date', verbose_name='Date', format='d-m-Y')
	distance = tables.Column(accessor='distance', verbose_name='Distance (km)')
	#selectmany = tables.CheckBoxColumn(checked=False)
	selectmany = tables.TemplateColumn(
			template_code='<input type="checkbox" name="checks" value="{{ record.id }}" />',
			verbose_name = 'Delete?',
			orderable=False
			)
	
		
	class Meta:
		model = Exercise
		attrs = {'class': 'paleblue'}
		fields = ('sport', 'time', 'distance', 'aver_speed', 'date', 'edit_entries', 'selectmany')
		sequence = ('sport', 'distance', 'time', 'aver_speed', 'date', 'edit_entries', 'selectmany')
	
	
	def get_bottom_pinned_data(self):
		""" """
		try:
			print("TASSA ON " + str(self.data))
			l = len(self.data)
			
			td = self.count_dist(self.data)
			#ad = self.avg_dist(self.data)
			ad = round(td/l, 2)
			
			tt = self.count_time(self.data)
			at = round(tt/l, 2)
			
			days = self.count_days(self.data)
		except ZeroDivisionError:
			td = ad = tt = at = days = 0 # No sports recorder, probably
			
			
		return [
			{
				'sport' : 'Total',
				'distance' : td, #self.tot_dis,
				'time' : str(round(tt,2)) + ' (h)',
				'date' : str(l) + '  records'
			},
			
			{
				'sport' : 'Average',
				'distance' : ad,
				'time' : str(at) + ' (h)',
				'date' : str(days) + ' days'
			}
		]
		
		
	def count_dist(self, tableQData):
		d = 0
		for i in tableQData:
			d = i.distance + d
		return d	
	
	def count_time(self, tableQData):
		t = 0
		for i in tableQData:
			t = i.time_as_hours + t
		return t
	
	
	def count_days(self, tableQData):
		"""Returns day differential of ordered queryset """
		d0 = tableQData[0].date
		dL = tableQData[len(tableQData)-1].date
		
		return ((d0 - dL).days)
	#def avg_time(self, tableQData):
	#	l = len(tableQData)
	#	return round(self.count_time(tableQData)/l, 2)
	#def render_aver_speed(self):#, record):
		#dis = float(record.distance)
		
		#minuts = int(record.hours)*60 + int(record.minutes)
	#	return str("Roki")#"Roki" #str(round(minuts/dis, 2))
	
		
	#def order_aver_speed(self, queryset):
		
	#	queryset = queryset.annotate(
	#		amount=average_speed()
	#		).order_by(amount)
	#	return (queryset, True)

class PersonTable(tables.Table):
	class Meta:
		model = Person
		attrs = {'class': 'paleblue'}
