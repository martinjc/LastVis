"""
Laspy Last.FM API library
"""
__version__ = '0.1'
__author__ = 'Martin Chorley'
__license__ = 'Apache v2.0'

from lastpy.error import LastpyError
from lastpy.auth_handler import LastpyAuthHandler
from lastpy.models import User, Album, Artist, Track, Library
from lastpy.api import API

