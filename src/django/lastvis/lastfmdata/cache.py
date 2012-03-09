import datetime
import hashlib
import pickle

from tweepy.cache import Cache
from lastvis.lastfmdata.models import CacheEntry


class DjangoDBCache( Cache ):

    def __init__( self, timeout = 60 ):
        """Initialize the cache
            model: django model type to use for storing cache entries
            timeout: number of seconds to keep a cached entry
        """
        self.timeout = datetime.timedelta( seconds = timeout )

    def store( self, key, value ):
        """Add new record to cache
            key: entry key
            value: data of entry
        """
        md5 = hashlib.md5()
        md5.update( key )
        cache_entry = CacheEntry( time = datetime.datetime.now(), key = md5.hexdigest(), value = pickle.dumps( value ) )
        cache_entry.save()

    def get( self, key, timeout = None ):
        """Get cached entry if exists and not expired
            key: which entry to get
            timeout: override timeout with this value [optional]
        """
        md5 = hashlib.md5()
        md5.update( key )
        key = md5.hexdigest()
        try:
            value = CacheEntry.objects.get( key = key )
            print 'CACHE: %s found in cache' % key
        except CacheEntry.DoesNotExist:
            print 'CACHE: %s not in cache' % key
            return None

        if timeout is None:
            timeout = self.timeout
        else:
            timeout = datetime.timedelta( seconds = timeout )
        if timeout >= datetime.timedelta( seconds = 0 ) and ( datetime.datetime.now() - value.time ) >= timeout:
            print 'CACHE: %s is old, deleting' % key
            value.delete()
            value = None
        else:
            value = pickle.loads( value.value )

        return value

    def count( self ):
        """Get count of entries currently stored in cache"""
        return CacheEntry.objects.count()

    def cleanup( self ):
        """Delete any expired entries in cache."""
        cache_entries = CacheEntry.objects.all()
        for entry in cache_entries:
            if ( datetime.datetime.now() - entry.time ) >= self.timeout:
                entry.delete()

    def flush( self ):
        """Delete all cached entries"""
        [ entry.delete() for entry in CacheEntry.objects.all() ]
