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

from lastfmauth.models import LastFMUser
from lastpy import LastpyAuthHandler, API
from cache import DjangoDBCache

ROOT_URL = getattr( settings, 'ROOT_URL', 'http://127.0.0.1:8000/' )
API_KEY = getattr( settings, 'API_KEY', '' )
API_SECRET = getattr( settings, 'API_SECRET', '' )


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
