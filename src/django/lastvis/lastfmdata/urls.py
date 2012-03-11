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

    url( r'charts/(?P<year>\d+)/$', view = yearly_chart, name = 'yearly_chart' ),
    url( r'charts/(?P<year>\d+)/(?P<month>\d+)/$', view = monthly_chart, name = 'monthly_chart' ),
    url( r'weeklychart/(?P<week>\w+)/$', view = weekly_chart, name = 'weekly_chart' ),

    url( r'topartists/$', view = top_artist_list, name = 'top_artists' ),
    url( r'toptracks/$', view = top_track_list, name = 'top_tracks' ),

    url( r'test/$', view = test, name = 'api_test' ),
    url( r'test2/$', view = test2, name = 'api_test' ),

 )
