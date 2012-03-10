# Create your views here.
# Create your views here.
import json
import logging
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
            cache = DjangoDBCache( timeout = 60 )
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

def weekly_chart( request, week ):
    api, user = get_api_and_user( request )

    genres = []
    weekly_chart_list = api.user_getweeklychartlist( user = user.user.username )

    week = weekly_chart_list.charts[int( week )]

    artists = api.user_getweeklyartistchart( user.user.username, week.start, week.end )

    for artist in artists.artists:
        logger.info( artist.name )
        artist_info = api.artist_getinfo( artist = artist.name )
        logger.info( artist_info.to_dict() )
        genres.append( artist_info.to_dict() )
        logger.info( genres )

    return return_data( request, {"chart" : genres} )

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
