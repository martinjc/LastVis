# Create your views here.
# Create your views here.
import json
import logging
import copy
import datetime
from django.http import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.views.decorators.csrf import csrf_exempt, requires_csrf_token

from lastvis.lastfmauth.models import LastFMUser
from lastvis.lastpy import LastpyAuthHandler, API
from cache import DjangoDBCache

ROOT_URL = getattr( settings, 'ROOT_URL', 'http://127.0.0.1:8000/' )
API_KEY = getattr( settings, 'API_KEY', '' )
API_SECRET = getattr( settings, 'API_SECRET', '' )

from test_json import chart

logger = logging.getLogger( 'lastvis.custom' )

def get_api_and_user( request ):

    session_key = request.session.get( 'session_key', None )
    if session_key is not None:

            auth = LastpyAuthHandler( request.session['session_key'], API_KEY, API_SECRET )
            cache = DjangoDBCache( timeout = 3600 )
            api = API( auth, cache = cache )

    user = request.user
    lastfm_user = user.get_profile()

    return api, lastfm_user

@login_required
def user_info( request, user_name = None ):

    api, user = get_api_and_user( request )

    if user_name is None:
        return_user = api.user_getinfo()
    else:
        return_user = api.user_getinfo( user = user_name )

    return HttpResponse( json.dumps( { 'user' : return_user.to_dict() } ), mimetype = 'application/json' )

def yearly_chart( request, year ):
    api, user = get_api_and_user( request )

    weekly_chart_list = api.user_getweeklychartlist( user = user.user.username )
    weeks = []

    year_start = datetime.datetime( year, 01, 01, 00, 00 )
    year_end = datetime.datetime( year, 12, 31, 23, 59 )

    year_start_epoch = time.mktime( year_start.timetuple() )
    year_end_epoch = time.mktime( year_end.timetuple() )
    for week in weekly_chart_list.charts:
        if week.start > year_start_epoch and week.start < year_end_epoch and week.end > year_start_epoch and week.end < year_end_epoch:
            weeks.append( week )

    return return_chart_data( request, api, user, weeks )

def monthly_chart( request, year, month ):
    api, user = get_api_and_user( request )

    weekly_chart_list = api.user_getweeklychartlist( user = user.user.username )
    weeks = []

    month_start = datetime.datetime( year, month, 01, 00, 00 )
    month_end = datetime.datetime( year, month, 31, 23, 59 )

    month_start_epoch = time.mktime( month_start.timetuple() )
    month_end_epoch = time.mktime( month_end.timetuple() )
    for week in weekly_chart_list.charts:
        if week.start > month_start_epoch and week.start < month_end_epoch and week.end > month_start_epoch and week.end < month_end_epoch:
            weeks.append( week )

    return return_chart_data( request, api, user, weeks )

def return_chart_data( request, api, user, weeks, ):
    genres = []

    artist_totals = []

    for week in weeks:
        artists = api.user_getweeklyartistchart( user.user.username, week.start, week.end )
        tracks = api.user_getweeklytrackchart( user.user.username, week.start, week.end )
        for artist in artists.artists:
            this_artist = None
            for artist_total in artist_totals:
                if artist_total['name'] == artist.name:
                    this_artist = artist_total
            if this_artist is None:
                this_artist = { 'name' : artist.name, 'playcount' : int( artist.playcount ), 'tracks': [] }
            else:
                this_artist['playcount'] += int( artist.playcount )


            for track in tracks.tracks:
                if this_artist['name'] == track.artist.name:
                    this_track = None
                    for track_total in artist['tracks']:
                        if track_total['name'] == track.name:
                            this_track = track_total
                    if this_track is None:
                        this_track = { 'name' : track.name, 'playcount' : int( track.playcount ) }
                        this_artist.tracks.append( this_track )
                    else:
                        this_track['playcount'] += int( track.playcount )

        for artist in artist_totals:
            artist_info = api.artist_getinfo( artist = artist['name'] )
            artist_genre = artist_info.tags.tag[0].name;

            this_genre = None
            for genre in genres:
                if genre['name'] == artist_genre:
                    this_genre = genre
            if this_genre is None:
                this_genre = { 'name' : artist_genre, 'playcount' : artist['playcount'], 'artists' : [] }
            else:
                this_genre['playcount'] += artist['playcount']

            this_genre['artists'].append( artist )

        return return_data( request, {'chart' : { 'genres' : genres }} )

def weekly_chart( request, week ):
    api, user = get_api_and_user( request )

    weekly_chart_list = api.user_getweeklychartlist( user = user.user.username )

    week = weekly_chart_list.charts[int( week )]

    return return_chart_data( request, api, user, [week] )

@login_required
def weekly_chart_list( request ):

    api, user = get_api_and_user( request )

    chart_list = api.user_getweeklychartlist( user = user.user.username )

    return return_data( request, chart_list.to_dict() )


def test( request ):

    return return_data( request, { "chart" : chart } )


def return_data( request, data_dict ):

    callback = request.GET.get( 'callback', None )

    if callback is None:
        return HttpResponse( json.dumps( data_dict ), mimetype = 'application/json' )
    else:
        return HttpResponse( callback + '(' + json.dumps( data_dict ) + ')', mimetype = 'application/javascript' )
