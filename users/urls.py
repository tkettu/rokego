"""Defines URL patterns for users."""

from django.conf.urls import url, include
from django.contrib.auth.views import login

from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # Login page
    url(r'^login/$', login, {'template_name': 'users/login.html'}, 
		name='login'),
	# Logout page
	url(r'^logout/$', views.logout_view, name='logout'),
    # Registration page
    url(r'^register/$', views.register, name='register'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    
    # Password reset
   
    url('^', include('django.contrib.auth.urls')),

    #url(r'^password_reset_form/$', views.password_reset_form, name='password_reset_form'),
    #url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    #url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    #url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #    auth_views.password_reset_confirm, name='password_reset_confirm'),
    #url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    #url('^', include('django.contrib.auth.urls')),
]
