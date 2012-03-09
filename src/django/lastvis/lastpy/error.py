class LastpyError( Exception ):
    """ Error with Lastpy """

    def __init__( self, error_code=None, error_message=None ):
        self.error_code = error_code
        self.error_message = error_message

    def __str__( self ):
        return u'%s: %s' % ( self.error_code, self.error_message )

class LastpyRequestError( LastpyError ):
    """ Error coming from Last.FM - an error from the API """
    pass