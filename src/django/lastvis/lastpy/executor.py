import urllib
import httplib
import logging

from lastpy.error import LastpyError
from lastpy.models import Model

logger = logging.getLogger( 'lastvis.custom' )

def bind_api( **config ):

    class APIMethod( object ):

        endpoint = config.get( 'endpoint' )
        allowed_params = config.get( 'allowed_params', None )
        required_params = config.get( 'required_params', None )
        method = config.get( 'method', 'GET' )
        require_auth = config.get( 'require_auth', False )
        use_cache = config.get( 'use_cache', True )

        def __init__( self, api, args, kargs ):

            # If authentication required and no authentication
            # handler supplied, throw an error

            if self.require_auth and not api.auth_handler:
                raise LastpyError( 1, 'Authentication required, but no authentication handler available' )

            self.api = api
            self.retry_count = kargs.pop( 'retry_count', api.retry_count )
            self.retry_errors = kargs.pop( 'retry_errors', api.retry_errors )
            self.headers = kargs.pop( 'headers', {} )
            self.build_parameters( args, kargs )

            # If user can be supplied to method but no user parameter supplied, add authentication
            # to API call so last.fm defaults to authenticated user
            if 'user' in self.allowed_params and api.auth_handler and not 'user' in self.parameters:
                self.require_auth = True
            elif 'user' in self.allowed_params and not api.auth_handler and not 'user' in self.parameters:
                raise LastpyError( 2, '"user" parameter not supplied and no authentication handler available' )

        def build_parameters( self, args, kargs ):

            self.parameters = {}

            for idx, arg in enumerate( args ):
                if arg is None:
                    continue

                try:
                    self.parameters[ self.allowed_params[ idx ] ] = arg
                except IndexError:
                    raise LastpyError( 'Too many parameters supplied!' )

            for k, arg in kargs.items():
                if arg is None:
                    continue

                if k in self.parameters:
                    raise LastpyError( 'Multiple values for parameter %s supplied!' % k )

                self.parameters[k] = arg

            # add the method to the parameters
            self.parameters['method'] = self.endpoint

        def execute( self ):

            # pause if necessary to observe API rate limiting
            self.api.rate_controller.control_rate()

            # build the url
            url = self.api.scheme + self.api.host + self.api.root

            # apply auth to call (add api key or full authentication)
            if self.api.auth_handler:
                self.api.auth_handler.apply_auth( url, self.headers, self.parameters, self.require_auth )

            # Query the cache if one is available
            # and this request uses a GET method.
            if self.use_cache and self.api.cache and self.method == 'GET':
                store_url = '%s?%s' % ( url, urllib.urlencode( self.parameters ) )
                cache_result = self.api.cache.get( store_url )
                # if cache result found and not expired, return it
                if cache_result:
                    logger.info( 'EXECUTOR: found in cache' )
                    if isinstance( cache_result, Model ):
                        cache_result.restore_api( self.api )
                    return cache_result
                else:
                    logger.info( 'EXECUTOR: not found in cache, hitting last.fm' )

            # parameters on url if GET, in post data if POST
            self.parameters['format'] = u'json'
            if self.method == 'GET':
                url = '%s?%s' % ( url, urllib.urlencode( self.parameters ).encode( 'utf-8' ) )
                self.post_data = urllib.urlencode( {} )
            else:
                self.headers['Content-type'] = u'application/x-www-form-urlencoded'
                self.post_data = urllib.urlencode( self.parameters )

            self.headers['User-Agent'] = 'LastVis:5e1aff6b88998e05c176abbd5118d6ba'

            logger.info( 'EXECUTOR: retrieving: %s' % url )
            retries_performed = 0
            while retries_performed < self.retry_count + 1:

                conn = httplib.HTTPConnection( self.api.host )

                try:
                    conn.request( self.method, url, headers = self.headers, body = self.post_data )
                    response = conn.getresponse()
                    data = response.read()
                except Exception as e:
                    raise e
                    raise LastpyError( 3, 'Error making API request' )

                # Exit request loop if non-retry error code
                if self.retry_errors:
                    if response.status not in self.retry_errors: break
                else:
                    if response.status == 200: break

                retries_performed += 1

            result = self.api.parser.parse( self, data )

            conn.close()

            if self.use_cache and self.api.cache and self.method == 'GET' and result:
                logger.info( 'EXECUTOR: storing result' )
                self.api.cache.store( store_url, result )

            return result

    def _call( api, *args, **kargs ):

        method = APIMethod( api, args, kargs )
        return method.execute()

    return _call



