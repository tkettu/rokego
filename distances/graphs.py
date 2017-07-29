""" Graphs.py , Handle graph view requests"""

from .models import Exercise

import matplotlib.pyplot as plt
import django

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import matplotlib.cm as cm

#import PIL, PIL.Image, StringIO

def graphs(request, sport='Running'):
	
	exercises = Exercise.objects.filter(owner=request.user, sport=sport)
	
	fig = Figure()
	ax = fig.add_subplot(111)
	d = []
	t = []
	cc = []
	for e in exercises:
		d.append(e.distance)
		t.append(e.time_as_hours)
		cc.append(e.sport)
	
	#plt.scatter(d,t)
	ax.plot(d,t)
	canvas = FigureCanvas(fig)
	response = django.http.HttpResponse(content_type='image/png')
	
	canvas.print_png(response)
	return response

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
	
	# TODO Take sports from JSON and assign colors
	color_dict = {'Running': 'green', 'Skiing': 'blue', 'Cycling': 'blue', 'Walking': 'black', 'Swimming': 'purple'}
	#plt.scatter(d,t)
	try:
		ax.scatter(d,t, c=[ color_dict[i] for i in cc])
	except KeyError:
		# plot without colors
		ax.scatter(d,t)
	
	canvas = FigureCanvas(fig)
	response = django.http.HttpResponse(content_type='image/png')
	
	canvas.print_png(response)
	return response
	#buffer = StringIO.StringIO()
	#canvas = pylab.get_current_fig_manager().canvas
	#canvas.draw()
	#pilImage = PIL.Image.fromstring("RGB", canvas.get_width_height(), canvas.tostring_rgb())
	#pilImage.save(buffer, "PNG")
	#pylab.close()
	
	# Send buffer in a http response the the browser with the mime type image/png set
	#return HttpResponse(buffer.getvalue(), mimetype="image/png")
	#plt.show()
	
