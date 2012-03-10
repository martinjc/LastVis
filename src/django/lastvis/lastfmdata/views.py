# Create your views here.
# Create your views here.
import json

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

@login_required
def weekly_chart_list( request ):

    api, user = get_api_and_user( request )

    chart_list = api.user_getweeklychartlist()

    callback = request.GET.get( 'callback', None )

    if callback is None:
        return HttpResponse( json.dumps( chart_list ), mimetype = 'application/json' )
    else:
        return HttpResponse( callback + '(' + json.dumps( chart_list ) + ')', mimetype = 'application/javascript' )


def test( request ):


    callback = request.GET.get( 'callback', None )

    if callback is None:
        return HttpResponse( json.dumps( { "chart": chart } ), mimetype = 'application/json' )
    else:
        return HttpResponse( callback + '(' + json.dumps( { "chart": chart } ) + ')', mimetype = 'application/javascript' )
