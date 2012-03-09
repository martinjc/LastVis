import base64
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CacheEntry( models.Model ):
    time = models.DateTimeField()
    key = models.CharField( max_length = 32, primary_key = True )
    _value = models.TextField( db_column = 'value', blank = True, null = True )

    def set_data( self, data ):
        self._value = base64.encodestring( data )

    def get_data( self ):
        return base64.decodestring( self._value )

    value = property( get_data, set_data )
