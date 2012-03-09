from django.conf.urls.defaults import *
from lastfmauth.views import *

urlpatterns = patterns( 'lastfmauth.views',

    #
    # auth call
    url( r'^$', view=auth, name='auth_auth' ),

    #
    # callback
    url( r'^callback/', view=callback, name='auth_return' ),

    #
    # logout
    url( r'^logout/$', view=unauth, name='auth_logout' ),
)