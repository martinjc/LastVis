from django.conf.urls.defaults import *
from lastvis.lastfmdata.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns( 'lastvis.lastfmdata.views',
    # Retrieve the user info
    #
    # GET Request
    #
    # usage: /user/<user_id>/
    #
    # params:
    #
    # user_name
    #
    url( r'user/(?P<user_name>\w+)/$', view = user_info, name = 'user_info' ),

    url( r'weeklychartlist/$', view = weekly_chart_list, name = 'weekly_chart_list' ),

    url( r'weeklychart/(?P<week>\d+)/$', view = weekly_chart, name = 'weekly_chart' ),

    url( r'test/$', view = test, name = 'api_test' ),

 )
