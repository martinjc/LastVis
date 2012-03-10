from django.conf.urls.defaults import *
from base.views import *

urlpatterns = patterns( 'base.views',

    #
    # main page
    url( r'^$', view = main, name = 'base_main' ),

    #
    # main page
    url( r'^processing/$', view = processing_test, name = 'base_processing' ),


    url( r'^weeklycharts/$', view = weekly_charts, name = 'weekly_charts' ),
 )
