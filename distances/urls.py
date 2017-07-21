"""Defines URL patterns for learning_logs."""

from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    # Home page
    url(r'^$', views.index, name='index'),
    # Page for exerises
    url(r'^exercises/$', views.exercises, name='exercises'),
    
    url(r'^exercises/exercise/$', views.exercise, name='exercise'),
    url(r'^exercise/(?P<exercisename>\w{0,50})/$', views.exercise, name='exercisename'),
    
    # page for adding new exercises
    url(r'^new_exercise/$', views.new_exercise, name='new_exercise'),
    #url(r'^new_exercise2/$', views.new_exercise_modal, name='new_exercise2'),
    
    # Page for displaying user records
    url(r'^records/$', views.records, name='records'),
    
    # Page for displaying user records
    url(r'^graphs/$', views.graphs, name='graphs'),
    
    # Page for editing an exercise
    url(r'^edit_exercise/(?P<exercise_id>\d+)/$', views.edit_exercise, name='edit_exercise'),

    ## Password reset
    url('^', include('django.contrib.auth.urls')),

    
    
    
]
