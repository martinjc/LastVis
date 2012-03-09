import json

from lastpy.models import ModelFactory, Model, List
from lastpy.error import LastpyError, LastpyRequestError

class Parser( object ):

    def parse( self, method, data ):

        raise NotImplementedError

class RawParser( Parser ):

    def __init__( self ):
        pass

    def parse( self, method, data ):
        return data

class JSONParser( Parser ):

    def parse( self, method, data ):
        try:
            json_data = json.loads( data )
        except Exception as e:
            raise LastpyError( 4, 'Failed to parse JSON payload: %s' % e )

        error_code = json_data.get( 'error', None )
        if error_code is not None:
            error_message = json_data['message']
            raise LastpyRequestError( error_code, error_message )

        return json_data

class ModelParser( JSONParser ):

    def __init__( self, model_factory=None ):
        self.model_factory = model_factory or ModelFactory

    def parse( self, method, data ):
        json_data = JSONParser.parse( self, method, data )

        if hasattr(json_data, 'items'):
            if len(json_data.items()) == 1:
                try:
                    model = getattr( self.model_factory, json_data.keys()[0] )
                    result = model.parse( method.api, json_data[json_data.keys()[0]] )
                except AttributeError as e:
                    result = List.parse( method.api, json_data[json_data.keys()[0]] )
                return result
            else:
                results = {}
                for k, v in json.items():
                    try:
                        model = getattr( self.model_factory, k )
                        results[k] =  model.parse( method.api, json_data[k] ) 
                    except AttributeError as e:
                        results[k] = List.parse( method.api, json_data[k] )
                return results
