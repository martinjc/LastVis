# Create your views here.
import urllib
import urllib2
import json
import hashlib

from django.http import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from models import LastFMUser


API_KEY = getattr( settings, 'API_KEY', '' )
API_SECRET = getattr( settings, 'API_SECRET', '' )

TOKEN_URL = 'http://www.last.fm/api/auth'
API_URL = 'http://ws.audioscrobbler.com/2.0/'

ROOT_URL = getattr( settings, 'ROOT_URL', 'http://127.0.0.1:8000/' )

def auth( request ):
    params = {
        'api_key' : API_KEY,
    }
    data = urllib.urlencode( params )
    return HttpResponseRedirect( '%s?%s' % ( TOKEN_URL, data ) )

def callback( request ):
    request_token = request.GET.get( 'token' )

    api_sig = hashlib.md5( 'api_key%smethodauth.getSessiontoken%s%s' % ( API_KEY, request_token, API_SECRET ) ).hexdigest()

    params = {
        'method' : 'auth.getSession',
        'api_key' : API_KEY,
        'token' : request_token,
        'api_sig' : api_sig,
        'format' : 'json',
    }

    data = urllib.urlencode( params )
    req = urllib2.Request( API_URL + '?' + data )

    response = urllib2.urlopen( req )
    session_key = json.loads( response.read() )['session']['key']

    request.session['session_key'] = session_key

    return HttpResponseRedirect( reverse( 'base_main' ) )

def unauth( request ):
    request.session.clear()
    logout( request )
    return HttpResponseRedirect( ROOT_URL )
