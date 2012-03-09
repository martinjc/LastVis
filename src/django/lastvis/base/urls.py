from django.conf.urls.defaults import *
from base.views import *

urlpatterns = patterns( 'base.views',

    #
    # main page
    url( r'^$', view=main, name='base_main' ),

)
