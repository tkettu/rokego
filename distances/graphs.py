""" Graphs.py , Handle graph view requests"""

from .models import Exercise
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import django

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import matplotlib.cm as cm
import matplotlib.patches as mpatches

import distances.json.sports as spo

from django.db.models import Min, Max
#import PIL, PIL.Image, StringIO

#def graphs(request, sport='Running'):
	
	#exercises = Exercise.objects.filter(owner=request.user, sport=sport)
	
	#fig = Figure()
	#ax = fig.add_subplot(111)
	#d = []
	#t = []
	#cc = []
	#for e in exercises:
		#d.append(e.distance)
		#t.append(e.time_as_hours)
		#cc.append(e.sport)
	
	##plt.scatter(d,t)
	#ax.plot(d,t)
	#canvas = FigureCanvas(fig)
	#response = django.http.HttpResponse(content_type='image/png')
	
	#canvas.print_png(response)
	#return response


color_list = ['b', 'g', 'r', 'c', 'm', 'y', 'black', 'brown', 'purple', 'gold', 'darkgray', 'azure']
sl = spo.get_sport_choices()
sport_list = [s[0] for s in sl]

def graphs2(exercises):
	
	
	fig = Figure()
	ax = fig.add_subplot(111)
	d = []
	t = []
	cc = []
	for e in exercises:
		d.append(e.distance)
		t.append(e.time_as_hours)
		cc.append(e.sport)
	
	
	
	
	color_dict = get_color_dict()
	try:
		ax.scatter(d,t, c=[ color_dict[i] for i in cc])
	except KeyError:
		# plot without colors
		ax.scatter(d,t)
	
	recs = []
	inds = list(set(cc))
	sl = get_sport_list()
	
	for i in inds:#range(0,len(set(cc))):  # legend color for unique sport values
		recs.append(mpatches.Rectangle((0,0),1,1,fc=color_list[sl.index(i)]))
	
	
	fig.legend( recs, inds, 'right')
	#fig.suptitle("Scatter plot")
	title = get_date_title(exercises)
	fig.suptitle(title)
	
	ax.set_xlabel('Distance')
	ax.set_ylabel('Time')
	#ax.get_xaxis().get_major_formatter().set_scientific(False)
	
	ax.get_xaxis().get_major_formatter().set_useOffset(False)
	ax.get_yaxis().get_major_formatter().set_useOffset(False)
	#fig.axes(x='distance', y='time')
	canvas = FigureCanvas(fig)
	response = django.http.HttpResponse(content_type='image/png')
	
	canvas.print_png(response)
	return response

def graph_dist_sum(exercises):
	""" Cumulative distance of exercises """
	fig = Figure()
	ax = fig.add_subplot(111)
	
	exes = exercises.order_by('date')
	
	dist = np.array([e.distance for e in exes])
	dat = [e.date for e in exes]
	cum_sum = np.cumsum(dist)
	
	ax.plot(dat,cum_sum)
	ax.set_xlabel('Date')
	ax.set_ylabel('Cumulative distance')
	
	fig.suptitle(get_date_title(exercises))
	canvas = FigureCanvas(fig)
	response = django.http.HttpResponse(content_type='image/png')
	
	canvas.print_png(response)
	return response
	
def box_plot(exercises, quant='distance'):
	"""Returns boxplot (whiskers) from distances (or time) of exercises """
	
	# exercises to list of sport name and distances
	el = list(exercises.values('sport', quant))
	
	#dd = []
	#for e in exercises:
	#	di = float(e.distance) # e.quant
	#	dd.append(di)
	
	# el to list of distances [['Running_distances'],['Walking_distances']]
	#sports = [
	# ell = []
	fig = Figure()
	ax = fig.add_subplot(111)
	
	
	#ax.boxplot(ell
	dd = {}
	for e in el:
		di = float(e['distance'])
		dd.setdefault(e['sport'], []).append(di)
	
	dl = []
	dk = []
	for k,v in dd.items():
		dk.append(k)
		dl.append(v)
	
	#ax.boxplot(dd)
	ax.boxplot(dl)
	
	ax.set_xticklabels( dk)
	ax.set_ylabel('Distance')
	fig.suptitle("Whisker {0}".format(get_date_title(exercises)))
	
	canvas = FigureCanvas(fig)
	response = django.http.HttpResponse(content_type='image/png')
	
	canvas.print_png(response)
	return response
	
	
def get_color_dict():
	sport_list = get_sport_list()
	cd = {}
	for i in range(len(sport_list)):
		cd[sport_list[i]] = color_list[i]
	
	return cd

def get_sport_list():
	sl = spo.get_sport_choices()
	sport_list = [s[0] for s in sl]	
	return sport_list
	
def get_date_title(exercises):
	""" Return min and max dates of exercises as string"""
	""" Format mindate - maxdate """
	mindate = exercises.aggregate(Min('date'))
	mindates = mindate['date__min']
	maxdate = exercises.aggregate(Max('date'))
	maxdates = maxdate['date__max']
	
	retval = mindates.strftime("%d.%m.%y") + '-' + maxdates.strftime("%d.%m.%y")
	return retval
	#return str(mindates) + '-' + str(maxdates)
