import hashlib

class AuthHandler(object):

    def apply_auth(self, url, method, headers, parameters, require_auth=False):
        raise NotImplementedError


class LastpyAuthHandler(AuthHandler):

    def __init__(self, session_token, api_key, api_secret ):
        self.session_token = session_token
        self.api_key = api_key
        self.api_secret = api_secret

    def apply_auth(self, url, headers, parameters, require_auth=False):
        parameters['api_key'] = self.api_key
        parameters['sk'] = self.session_token
        if require_auth:
            signature = ''  
            for key in sorted( parameters.iterkeys( ) ):
                signature = '%s%s%s' % ( signature, key, parameters[key] )

            signature = '%s%s' % ( signature, self.api_secret )
            signature = hashlib.md5( signature ).hexdigest( )
            parameters['api_sig'] = signature