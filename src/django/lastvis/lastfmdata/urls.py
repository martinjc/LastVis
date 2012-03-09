from django.conf.urls.defaults import *
from lastfmdata.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns( 'lastfmdata.views',
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

 )
