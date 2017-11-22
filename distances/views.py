from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django_tables2 import RequestConfig

from django.db.models import Sum

from .models import Exercise
from .forms import (
    ExerciseForm,
    ExerciseFilterFormHelper, RecordFilterFormHelper,
    EditExerciseForm, GraphFilterFormHelper
)
from .tables import ExerciseTable
from distances.filters import ExerciseFilter, RecordFilter, GraphFilter

from distances.helpers.stats import Stats

import distances.helpers.records as rec
import distances.json.sports as spo

import distances.graphs as gra

from datetime import datetime, date

import logging

# Debugging
# import pdb; pdb.set_trace()

logger = logging.getLogger(__name__)

exercise_name = 'all'
end_date = ''
start_date = ''


def index(request):
    """The home page for Distance Tracker."""

    if request.user.is_authenticated():
        today = date.today()
        cur_week = today.isocalendar()[1]
        cur_month = today.month
        cur_year = today.year
        exercises_week = Exercise.objects.filter(owner=request.user,
                                            date__week=cur_week, date__year=cur_year).all().order_by('-date')

        exercises_month = Exercise.objects.filter(owner=request.user,
                                              date__month=cur_month, date__year=cur_year).all().order_by('-date')

        exes10 = Exercise.objects.filter(owner=request.user).all().order_by('-date')[:10]
        distance_week = Stats.totals(exercises_week)
        time_week = Stats.totaltime(exercises_week)

        distance_month = Stats.totals(exercises_month)
        time_month = Stats.totaltime(exercises_month)

        ret_url = 'distances:index'
        if request.method != 'POST':
            form = ExerciseForm()

        else:
            modaln = new_exercise_modal(request, ret_url)
            if modaln[1]:
                return HttpResponseRedirect(reverse(modaln[2]))
            form = modaln[0]

        context = {'dist': distance_week, 'time': time_week, 'distm': distance_month,
                   'timem': time_month, 'exercises': exes10, 'form': form,
                   'subsports': spo.get_sports_json()}

    else:
        context = {'link': 'https://www.youtube.com/watch?v=tENiCpaIk9A'}

    return render(request, 'distances/index.html', context)


@login_required
def exercises(request):
    context = {}
    exercises = Exercise.objects.filter(owner=request.user).all().order_by('-date')

    filter = ExerciseFilter(request.GET, queryset=exercises)
    filter.form.helper = ExerciseFilterFormHelper()
    filtered_exercises = filter.qs

    # Add new exercise with modal
    ret_url = 'distances:exercises'
    if request.method != 'POST':

        form = ExerciseForm()

    else:

        if request.POST.get('delete'):
            # TODO, implement working multi delete

            items = request.POST.getlist('checks')

        modaln = new_exercise_modal(request, ret_url)
        if modaln[1]:
            return HttpResponseRedirect(reverse(modaln[2]))
        form = modaln[0]

    table = ExerciseTable(filtered_exercises)

    # set totals, averages etc. table.set...(Stats.get...)
    RequestConfig(request).configure(table)
    context['filter'] = filter
    context['table'] = table
    # context['form'] = modalForm
    context['form'] = form
    context['subsports'] = spo.get_sports_json()
    response = render(request, 'distances/exercises.html', context)
    return response


def new_exercise_modal(request, ret_url):
    form = ExerciseForm(data=request.POST)

    isForm = False
    if form.is_valid():
        new_exercise = form.save(commit=False)
        new_exercise.owner = request.user
        check_numberfields(new_exercise)
        new_exercise.save()

        if request.POST.get("submit"):
            isForm = True
        # return HttpResponseRedirect(reverse(ret_url))
        elif request.POST.get("submitother"):
            msg = 'Added ' + str(new_exercise.sport) + ' ' + str(new_exercise.distance) + ' km.'
            ret_url = 'distances:new_exercise'
            isForm = True
            # return HttpResponseRedirect(reverse('distances:new_exercise'))
    return [form, isForm, ret_url]


def check_numberfields(ex):
    if ex.hours is None:
        ex.hours = 0
    if ex.minutes is None:
        ex.minutes = 0
    if ex.distance is None:
        ex.distance = 0


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
            check_numberfields(new_exercise)
            new_exercise.save()

            logger.warning(request.POST)
            # if request.POST.get("addone", "submit"):
            if request.POST.get("submit"):
                logger.warning('Going back to exercises?')
                return HttpResponseRedirect(reverse('distances:exercises'))
            elif request.POST.get("submitother"):
                # Inform somehow that new was added
                logger.warning('Going to new_exercises?')
                msg = 'Added ' + str(new_exercise.sport) + ' ' + str(new_exercise.distance) + ' km.'
                messages.info(request, msg)
                return HttpResponseRedirect(reverse('distances:new_exercise'))

    context = {'form': form, 'subsports': spo.get_sports_json()}
    return render(request, 'distances/new_exercise.html', context)


@login_required
def stats(request):
    """ Display different records"""
    context = {}

    # TODO this not good
    # defyear = 2017
    data = request.GET.copy()

    if len(data) == 0:
        default_year = datetime.now().year
    elif data['year'] == '':
        default_year = datetime.now().year
    else:
        default_year = request.GET.get('year')

    exercises = Exercise.objects.filter(owner=request.user, date__year=default_year).all().order_by('-date')

    record_filter = RecordFilter(request.GET, queryset=exercises)
    record_filter.form.helper = RecordFilterFormHelper()

    ddays = [7, 30, 365]  # , filter.get_days()]
    recs = []

    # Todo optimize longest period, now this is like O(n^2)
    # for d in ddays:
    #	re0 = rec.longest_period(filter.qs, days=d)
    #	recs.append(re0)

    context['yearnro'] = default_year
    context['year'] = record_filter.qs.aggregate(Sum('distance'))['distance__sum']
    context['yeartime'] = Stats.totaltime(record_filter.qs)  # filter.qs.aggregate(Sum('time_as_hours'))['time_as_hours__sum']
    weeks = rec.week_results(record_filter.qs)
    # recs = rec.longest_period(request.user, days=7, sport='Running')
    context['filter'] = record_filter
    # context['recs'] = recs
    context['weeks'] = weeks
    context['months'] = rec.month_results(record_filter.qs)
    # context['month'] = months

    # context = {'form': form, 'recs': recs, 'weeks': weeks, 'ename': sport}
    return render(request, 'distances/stats.html', context)


@login_required
def edit_exercise(request, exercise_id):
    """Edit en existing entry"""
    entry = Exercise.objects.get(id=exercise_id)

    cur_user = request.user
    check_exercise_owner(entry, cur_user)
    if request.method != 'POST':
        # Initial request; pre-fill form from the current entry.
        form = EditExerciseForm(instance=entry, sport=entry.sport, sub_sport=entry.sub_sport)
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
    exercises = Exercise.objects.filter(owner=cur_user, sport='NOSPORT').all().order_by('-date')
    for s in names:
        ex = Exercise.objects.filter(owner=cur_user, sport=s).all().order_by('-date')
        exercises = exercises | ex

    return exercises

@login_required
def exercise(request, exercisename):
    """Show single sport and its totals."""

    e = exercisename
    cur_user = request.user
    exercises = Exercise.objects.filter(owner=cur_user, sport=e).order_by('-date')
    context = {'exercises': exercises, 'total': Stats.total(cur_user, sport=e),
               'totaltime': Stats.totaltime(cur_user, sport=e)}
    return render(request, 'distances/exercises.html', context)


######## GRAPHS #########

# pattern for splitting multiple sports and dates from graphs to image
ptr = 'AND'
sptr = 'SDATE'
eptr = 'EDATE'
gptr = 'GTYPE'
default_graph = ''

def set_default_graph(graph_type):
    global default_graph
    default_graph = graph_type

@login_required
def graphs(request):
    """ Display graphs"""
    context = {}

    exercises = Exercise.objects.filter(owner=request.user).all().order_by('-date')

    graph_filter = GraphFilter(request.GET, queryset=exercises)
    graph_filter.form.helper = GraphFilterFormHelper()

    context['filter'] = graph_filter

    sport_request = request.GET.getlist('sport')
    start_date_req = request.GET.get('startDate')
    end_date_req = request.GET.get('endDate')

    graph_type = request.GET.get('graphType')

    if (graph_type != 'e'):
        set_default_graph(graph_type)

    context['image'] = set_image_filter(sport_request, start_date_req, end_date_req, graph_type)

    return render(request, 'distances/graphs.html', context)


def set_image_filter(sport="", start_date="", end_date="", graph_type="s"):
    start_date = str(start_date)
    end_date = str(end_date)
    if (sport == "") & (start_date == "") & (end_date == ""):
        ret_str = 'None'
    else:
        if len(sport) != 0:
            req = ''
            for i in sport:
                req = req + i + ptr
            ret_str = req + sptr + start_date + eptr + end_date
        else:
            ret_str = sptr + start_date + eptr + end_date

    if not isinstance(default_graph, str):
        if isinstance(graph_type,str):
            return ret_str + gptr + graph_type
        else:
            return ret_str + gptr + "s"
    else:
        return ret_str + gptr + default_graph


@login_required
def image(request, filters):
    """Build image by filters
        Format of '<Sport1>ptr<Sport2>ptr...<SportN>ptr+sptr<start_date>sptr<end_date>gptr<t>'
        We split filters for sports, dates and graphtype and call corresponding graph with filters"""

    if (filters != 'None'):  # & (filters != ''):
        sports = filters.split(ptr)         #  [<sport1>,<sport2>,...,<sportN>,sptr<start_date>eptr<end_date>gptr<t>]
        dates = sports[-1]                  #  sptr<start_date>eptr<end_date>gptr<t>
        sports = sports[:-1]                #  [<sport1>,<sport2>,...,<sportN>]
        dates = dates.replace(sptr, eptr)   #  eptr<start_date>eptr<end_date>gptr<t>
        dates = dates.split(eptr)           #  ['', <start_date>,<end_date>gptr<t>]
        # dates[0] is (hopefully) always ''
        sd = dates[1]
        ed = dates[2]                       #  <end_date>gptr<t>

        gtype = ed.split(gptr)              #  [<end_date>,<t>]
        ed = gtype[0]
        gtype = gtype[1]

        if (ed == 'None') | (ed == ''):
            ed = date.today()
        if (sd == 'None') | (sd == ''):
            # if type(sd) != date:
            if isinstance(ed, str):
                ed = datetime.strptime(ed, '%Y-%m-%d').date()
            sd = date(ed.year, 1, 1)
        # sd = date(date.today().year, 1, 1)

        if len(sports) != 0:
            exercises = Exercise.objects.filter(owner=request.user, sport__in=sports,
                                                date__range=[sd, ed]).all().order_by('-date')
        else:
            exercises = Exercise.objects.filter(owner=request.user,
                                                date__range=[sd, ed]).all().order_by('-date')
    else:
        exercises = Exercise.objects.filter(owner=request.user).all().order_by('-date')

    if gtype == 's':
        response = gra.graphs2(exercises)
    elif gtype == 'c':
        response = gra.graph_dist_sum(exercises)
    elif gtype == 'b':
        response = gra.box_plot(exercises)
    else:
        response = gra.graphs2(exercises)

    return response


def check_exercise_owner(exercise, user):
    if exercise.owner != user:
        raise Http404
    return True


def get_stats(cur_user, sport='all'):
    """ method for averages total ..."""
