# Create your views here.
from django.http import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from lastvis.lastfmauth.models import LastFMUser
from lastvis.lastpy import LastpyAuthHandler, API

ROOT_URL = getattr( settings, 'ROOT_URL', 'http://127.0.0.1:8000/' )
API_KEY = getattr( settings, 'API_KEY', '' )
API_SECRET = getattr( settings, 'API_SECRET', '' )

def main( request ):
    if request.user.is_authenticated():
        user = request.user
        lastfm_user = user.get_profile()
        return render_to_response( 'main.html', { 'lastfmuser' : lastfm_user, 'root_url' : ROOT_URL }, context_instance = RequestContext( request ) )
    else:
        if request.session.get( 'session_key' ) is not None:

            auth = LastpyAuthHandler( request.session['session_key'], API_KEY, API_SECRET )
            api = API( auth )

            data = api.user_getinfo()
            print data

            try:
                user = User.objects.get( username = data.name )
            except User.DoesNotExist:
                user = User.objects.create_user( username = data.name, email = '', password = '' )
                user.save()

            images = data.images
            for image in images:
                if image.size == u'large':
                    img = image.url

            user, created = LastFMUser.objects.get_or_create( user = user, defaults = {
                                    'url' : data.url,
                                    'image' : img,
                                    'playcount' : data.playcount } )
            user = authenticate( username = data.name, password = '' )
            login( request, user )
            lastfm_user = user.get_profile()
            return render_to_response( 'main.html', { 'lastfmuser' : lastfm_user, 'root_url' : ROOT_URL }, context_instance = RequestContext( request ) )
        else:
            return render_to_response( 'main.html', { 'root_url' : ROOT_URL }, context_instance = RequestContext( request ) )
