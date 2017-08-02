""" Graphs.py , Handle graph view requests"""

from .models import Exercise
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import django

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import matplotlib.cm as cm
import matplotlib.patches as mpatches

import distances.json.sports as spo
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
	fig.suptitle("Roki")
	
	ax.set_xlabel('Distance')
	ax.set_ylabel('Time')
	#fig.axes(x='distance', y='time')
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
	
	
