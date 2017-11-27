""" Graphs.py , Handle graph view requests"""

from .models import Exercise
import numpy as np
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

import django

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import matplotlib.patches as mpatches

import distances.json.sports as spo

from django.db.models import Min, Max

color_list = ['b', 'g', 'r', 'c', 'm', 'y', 'black', 'brown', 'purple', 'gold', 'darkgray', 'azure']

dist_label = 'distance (km)'
time_label = 'time (h)'


def graphs2(exercises):
    """ Scatter (time-distance) plot from exercises"""

    fig = Figure()
    ax = fig.add_subplot(111)
    distances = []
    times = []
    sports = []
    sport_types = []
    for e in exercises:
        distances.append(e.distance)
        times.append(e.time_as_hours)
        sports.append(e.sport)
        sport_types.append(e.sub_sport)

    recs = []
    sport_names = list(set(sports))

    nsports = len(sport_names)

    color_dict = get_color_dict(sport_names)

    if nsports > 1:
        sport_list = get_sport_list()
        coloring_sports = sports

    else:
        s_type = sport_names[0]
        coloring_sports = make_sub_sport_list(sport_types, s_type)
        sub_sport_names = list(set(coloring_sports))

        sport_list = get_sub_sport_list(s_type)

    try:
        # ax.scatter(d,t, c=[ color_dict[i] for i in cc])
        ax.scatter(distances, times, c=[color_dict[i] for i in coloring_sports])
    except KeyError:
        # plot without colors
        ax.scatter(distances, times)

    if nsports > 1:
        for i in sport_names:  # range(0,len(set(cc))):  # legend color for unique sport values
            recs.append(mpatches.Rectangle((0, 0), 1, 1, fc=color_list[sport_list.index(i)]))
        fig.legend(recs, sport_names, 'right')
    else:
        for i in sub_sport_names:
            recs.append(mpatches.Rectangle((0, 0), 1, 1, fc=color_list[sport_list.index(i)]))
        fig.legend(recs, sub_sport_names, 'right')

    title = get_date_title(exercises)
    fig.suptitle(title)

    ax.set_xlabel(dist_label)
    ax.set_ylabel(time_label)

    ax.get_xaxis().get_major_formatter().set_useOffset(False)
    ax.get_yaxis().get_major_formatter().set_useOffset(False)
    # fig.axes(x='distance', y='time')
    return graph_response(fig)


def graph_dist_sum(exercises):
    """ Cumulative distance of exercises """
    fig = Figure()
    ax = fig.add_subplot(111)

    exes = exercises.order_by('date')

    dist = np.array([e.distance for e in exes])
    date = [e.date for e in exes]

    cum_sum = np.cumsum(dist)

    ax.plot(date, cum_sum)
    ax.set_xlabel('Date')
    ax.set_ylabel('Cumulative distance (km)')
    fig.autofmt_xdate()
    fig.suptitle(get_date_title(exercises))

    return graph_response(fig)


def box_plot(exercises, quant='distance'):
    """Returns boxplot (whiskers) from distances (or time) of exercises """

    # exercises to list of sport name and distances/times
    # exercise_list = list(
    #     exercises.values('sport', quant))


    quant_list = {}

    if(quant == 'distance'):
        for e in exercises:
            quant_list.setdefault(e.sport,[]).append(float(e.distance))
    else:
        for e in exercises:
            quant_list.setdefault(e.sport,[]).append(float(e.time_as_hours))

    quantities = []
    names = []
    for k, v in quant_list.items():
        names.append(k)
        quantities.append(v)

    # ax.boxplot(distances)

    fig = Figure()
    ax = fig.add_subplot(111)
    ax.boxplot(quantities)

    ax.set_xticklabels(names)
    ylabel =  dist_label if quant=='distance' else time_label

    ax.set_ylabel(ylabel)
    fig.suptitle("Whisker {0}".format(get_date_title(exercises)))

    return graph_response(fig)


def graph_histogram(exercises, quant='distance'):
    """Histogram of quantity for distances/times"""

    dist = np.array([float(e.distance) for e in exercises])
    fig = Figure()
    ax = fig.add_subplot(111)
    n,bins, patches = ax.hist(dist, 50, facecolor='green', alpha=0.75)
    xlabel = dist_label if quant == 'distance' else time_label
    ax.grid(True)
    ax.set_xlabel(xlabel)

    return graph_response(fig)


def graph_response(fig):
    canvas = FigureCanvas(fig)
    response = django.http.HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response


def get_color_dict(sports):
    if len(sports) > 1:
        sport_list = get_sport_list()
    else:
        sport_list = get_sub_sport_list(sports[0])

    color_dict = {}
    for i in range(len(sport_list)):
        color_dict[sport_list[i]] = color_list[i]

    return color_dict


def get_sport_list():
    sl = spo.get_sport_choices()
    sport_list = [s[0] for s in sl]
    return sport_list


def get_sub_sport_list(s):
    sl = spo.getFieldChoices(key_field=s)

    sport_list = [s[0] for s in sl]
    sport_list[0] = s

    return sport_list


def make_sub_sport_list(sport_list, name):
    """ Fills empty and non-rights values in list sport_list with sport name"""
    slist = get_sub_sport_list(name)
    nlist = []
    for i in sport_list:
        if (i not in slist) | (i == ""):
            nlist.append(name)
        else:
            nlist.append(i)
    return nlist


def get_date_title(exercises):
    """ Return min and max dates of exercises as string"""
    """ Format mindate - maxdate """
    mindate = exercises.aggregate(Min('date'))
    mindates = mindate['date__min']
    maxdate = exercises.aggregate(Max('date'))
    maxdates = maxdate['date__max']

    retval = mindates.strftime("%d.%m.%y") + '-' + maxdates.strftime("%d.%m.%y")
    return retval

# return str(mindates) + '-' + str(maxdates)
