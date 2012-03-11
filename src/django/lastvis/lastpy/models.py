import inspect
import pickle

class Model( object ):

    members = {}

    def __init__( self, api = None ):
        self._api = api

    def __getstate__( self ):
        # pickle
        pickle = dict( self.__dict__ )
        try:
            del pickle['_api']  # do not pickle the API reference
        except KeyError:
            pass
        return pickle

    def restore_api( self, api ):

        self._api = api

        members = inspect.getmembers( self, inspect.isclass )
        for name, member in members:
            if isinstance( member, Model ):
                member.restore_api( api )

    def set_cache( self, cache ):

        if( self._api ):
            self._api.cache = cache


    @classmethod
    def parse( cls, api, json_data ):
        obj = cls( api )
        if hasattr( json_data, 'items' ):
            for k, v in json_data.items():
                k = k.lstrip( '@' ).lstrip( '#' )
                try:
                    model = getattr( ModelFactory, k )
                    if isinstance( v, list ):
                        results = []
                        for item in v:
                            results.append( model.parse( api, item ) )
                        k = cls.members.get( k, k )
                        setattr( obj, k, results )
                    else:
                        k = cls.members.get( k, k )
                        setattr( obj, k, model.parse( api, v ) )
                except AttributeError:
                    k = cls.members.get( k, k )
                    setattr( obj, k, Model.parse( api, v ) )
        else:
            return json_data
        return obj

    def to_dict( self, d = {} ):
        if hasattr( self, '__dict__' ):
            pickle = self.__getstate__()
            for k, v in pickle.iteritems():
                if isinstance( v, list ):
                    l = []
                    for item in v:
                        l.append( item.to_dict( {} ) )
                    d[k] = l
                elif isinstance( v, Model ):
                    d[k] = v.to_dict( {} )
                else:
                    d[k] = v
            return d
        else:
            d[self.__class__.__name__] = self
            return d

class User( Model ):

    members = {
        'image' : 'images'
    }

    def info( self, **kargs ):
        return self._api.user_getinfo( user = self.name, **kargs )

    def weeklychartlist( self, **kargs ):
        return self._api.user_getweeklychartlist( user = self.name, **kargs )

    def weeklyalbumchart( self, **kargs ):
        return self._api.user_getweeklyalbumchart( user = self.name, **kargs )

    def weeklyartistchart( self, **kargs ):
        return self._api.user_getweeklyartistchart( user = self.name, **kargs )

    def weeklytrackchart( self, **kargs ):
        return self._api.user_getweeklytrackchart( user = self.name, **kargs )

    def toptracks( self, **kargs ):
        return self._api.user_gettoptracks( user = self.name, **kargs )

    def topartists( self, **kargs ):
        return self._api.user_gettopartists( user = self.name, **kargs )

    def topalbums( self, **kargs ):
        return self._api.user_gettopalbums( user = self.name, **kargs )

    def toptags( self, **kargs ):
        return self._api.user_gettoptags( user = self.name, **kargs )

    def artisttracks( self, **kargs ):
        return self._api.user_getartisttracks( user = self.name, **kargs )

    def bannedtracks( self, **kargs ):
        return self._api.user_getbannedtracks( user = self.name, **kargs )

    def events( self, **kargs ):
        return self._api.user_getevents( user = self.name, **kargs )

    def friends( self, **kargs ):
        return self._api.user_getfriends( user = self.name, **kargs )

    def lovedtracks( self, **kargs ):
        return self._api.user_getlovedtracks( user = self.name, **kargs )

    def neighbours( self, **kargs ):
        return self._api.user_getneighbours( user = self.name, **kargs )

    def newreleases( self, **kargs ):
        return self._api.user_getnewreleases( user = self.name, **kargs )

    def pastevents( self, **kargs ):
        return self._api.user_getpastevents( user = self.name, **kargs )

    def personaltags( self, **kargs ):
        return self._api.user_getpersonaltags( user = self.name, **kargs )

    def getplaylists( self, **kargs ):
        return self._api.user_getplaylists( user = self.name, **kargs )

    def recentstations( self, **kargs ):
        return self._api.user_getrecentstations( user = self.name, **kargs )

    def recenttracks( self, **kargs ):
        return self._api.user_getrecenttracks( user = self.name, **kargs )

    def recommendedartists( self, **kargs ):
        return self._api.user_getrecommendedartists( **kargs )

    def recommendedevents( self, **kargs ):
        return self._api.user_getrecommendedevents( user = self.name, **kargs )

    def shouts( self, **kargs ):
        return self._api.user_getshouts( user = self.name, **kargs )

    def shout( self, **kargs ):
        return self._api.user_shout( **kargs )

class Image( Model ):

    members = {
        'text' : 'url',
        'image': 'images'
    }

class Library( Model ):

    def __init__( self, user, api = None ):
        self.user = user
        self._api = api

    def tracks( self, **kargs ):
        return self._api.library_gettracks( user = self.user.name, **kargs )

    def artists( self, **kargs ):
        return self._api.library_getartists( user = self.user.name, **kargs )

    def albums( self, **kargs ):
        return self._api.library_getalbums( user = self.user.name, **kargs )

    def addartist( self, **kargs ):
        return self._api.library_addartist( **kargs )

    def addtrack( self, **kargs ):
        return self._api.library_addtrack( **kargs )

    def addalbum( self, **kargs ):
        return self._api.library_addalbum( **kargs )

    def removeartist( self, **kargs ):
        return self._api.library_removeartist( **kargs )

    def removetrack( self, **kargs ):
        return self._api.library_removetrack( **kargs )

    def removealbum( self, **kargs ):
        return self._api.library_removealbum( **kargs )

    def removescrobble( self, **kargs ):
        return self._api.library_removescrobble( **kargs )

class Chart( Model ):

    members = {
        'chart' : 'charts',
        'from' : 'start',
        'to' : 'end'
    }

    def hypedartists( self, **kargs ):
        return self._api.chart_gethypedartists( **kargs )

    def hypedtracks( self, **kargs ):
        return self._api.chart_gethypedtracks( **kargs )

    def lovedtracks( self, **kargs ):
        return self._api.chart_getlovedtracks( **kargs )

    def topartists( self, **kargs ):
        return self._api.chart_gettopartists( **kargs )

    def toptags( self, **kargs ):
        return self._api.chart_gettoptags( **kargs )

    def toptracks( self, **kargs ):
        return self._api.chart_gettoptracks( **kargs )

class Album( Model ):

    members = {
        '#text' : 'name',
        'image' : 'images'
    }

    def addtags( self, **kargs ):
        if hasattr( self.artist, 'name' ):
            return self._api.album_addtags( artist = self.artist.name, album = self.name, **kargs )
        else:
            return self._api.album_addtags( artist = self.artist, album = self.name, **kargs )

    def buylinks( self, **kargs ):
        if hasattr( self.artist, 'name' ):
            return self._api.album_getbuylinks( artist = self.artist.name, album = self.name, **kargs )
        else:
            return self._api.album_getbuylinks( artist = self.artist, album = self.name, **kargs )

    def info( self, **kargs ):
        if hasattr( self.artist, 'name' ):
            return self._api.album_getinfo( artist = self.artist.name, album = self.name, **kargs )
        else:
            return self._api.album_getinfo( artist = self.artist, album = self.name, **kargs )

    def shouts( self, **kargs ):
        if hasattr( self.artist, 'name' ):
            return self._api.album_getshouts( artist = self.artist.name, album = self.name, **kargs )
        else:
            return self._api.album_getshouts( artist = self.artist, album = self.name, **kargs )

    def tags( self, **kargs ):
        if hasattr( self.artist, 'name' ):
            return self._api.album_gettags( artist = self.artist.name, album = self.name, **kargs )
        else:
            return self._api.album_gettags( artist = self.artist, album = self.name, **kargs )

    def gettoptags( self, **kargs ):
        if hasattr( self.artist, 'name' ):
            return self._api.album_gettoptags( artist = self.artist.name, album = self.name, **kargs )
        else:
            return self._api.album_gettoptags( artist = self.artist, album = self.name, **kargs )

    def removetag( self, **kargs ):
        if hasattr( self.artist, 'name' ):
            return self._api.album_removetag( artist = self.artist.name, album = self.name, **kargs )
        else:
            return self._api.album_removetag( artist = self.artist, album = self.name, **kargs )

    def share( self, **kargs ):
        if hasattr( self.artist, 'name' ):
            return self._api.album_share( artist = self.artist.name, album = self.name, **kargs )
        else:
            return self._api.album_share( artist = self.artist, album = self.name, **kargs )

    def search( self, **kargs ):
        return self._api.album_search( **kargs )

class Artist( Model ):

    members = {
        'text' : 'name',
        'image' : 'images',
    }

    def getinfo( self, **kargs ):
        return self._api.artist_getinfo( artist = self.name, **kargs )

    def addtags( self, **kargs ):
        return self._api.artist_addtags( artist = self.name, **kargs )

    def gettags( self, **kargs ):
        return self._api.artist_gettags( artist = self.name, **kargs )

    def removetag( self, **kargs ):
        return self._api.artist_removetag( artist = self.name, **kargs )

    def correction( self, **kargs ):
        return self._api.artist_getcorrection( **kargs )

    def events( self, **kargs ):
        return self._api.artist_getevents( artist = self.name, **kargs )

    def getimages( self, **kargs ):
        return self._api.artist_getimages( artist = self.name, **kargs )

    def pastevents( self, **kargs ):
        return self._api.artist_getpastevents( artist = self.name, **kargs )

    def getsimilar( self, **kargs ):
        return self._api.artist_getsimilar( artist = self.name, **kargs )

    def shouts( self, **kargs ):
        return self._api.artist_getshouts( artist = self.name, **kargs )

    def topalbums( self, **kargs ):
        return self._api.artist_gettopalbums( artist = self.name, **kargs )

    def toptags( self, **kargs ):
        return self._api.artist_gettoptags( artist = self.name, **kargs )

    def toptracks( self, **kargs ):
        return self._api.artist_gettoptracks( artist = self.name, **kargs )

    def topfans( self, **kargs ):
        return self._api.artist_gettopfans( artist = self.name, **kargs )

    def share( self, **kargs ):
        return self._api.artist_share( artist = self.name, **kargs )

    def search( self, **kargs ):
        return self._api.artist_search( **kargs )

    def shout( self, **kargs ):
        return self._api.artist_shout( artist = self.name, **kargs )

    def podcast( self, **kargs ):
        return self._api.artist_getpodcast( artist = self.name, **kargs )

class Track( Model ):

    members = {
        'image' : 'images'
    }

    def addtags( self, **kargs ):
        if hasattr( self.artist, 'name' ):
            return self._api.track_addtags( artist = self.artist.name, track = self.name, **kargs )
        else:
            return self._api.track_addtags( artist = self.artist, track = self.name, **kargs )

    def ban( self, **kargs ):
        if hasattr( self.artist, 'name' ):
            return self._api.track_ban( artist = self.artist.name, track = self.name, **kargs )
        else:
            return self._api.track_ban( artist = self.artist, track = self.name, **kargs )

    def buylinks( self, **kargs ):
        if hasattr( self.artist, 'name' ):
            return self._api.track_getbuylinks( artist = self.artist.name, track = self.name, **kargs )
        else:
            return self._api.track_getbuylinks( artist = self.artist, track = self.name, **kargs )

    def correction( self, **kargs ):
        if hasattr( self.artist, 'name' ):
            return self._api.track_getcorrection( artist = self.artist.name, track = self.name, **kargs )
        else:
            return self._api.track_getcorrection( artist = self.artist, track = self.name, **kargs )

    def fingerprintmetadata( self, **kargs ):
        if hasattr( self.artist, 'name' ):
            return self._api.track_getfingerprintmetadata( artist = self.artist.name, track = self.name, **kargs )
        else:
            return self._api.track_getfingerprintmetadata( artist = self.artist, track = self.name, **kargs )

    def info( self, **kargs ):
        if hasattr( self.artist, 'name' ):
            return self._api.track_getinfo( artist = self.artist.name, track = self.name, **kargs )
        else:
            return self._api.track_getinfo( artist = self.artist, track = self.name, **kargs )

    def shouts( self, **kargs ):
        if hasattr( self.artist, 'name' ):
            return self._api.track_getshouts( artist = self.artist.name, track = self.name, **kargs )
        else:
            return self._api.track_getshouts( artist = self.artist, track = self.name, **kargs )

    def similar( self, **kargs ):
        if hasattr( self.artist, 'name' ):
            return self._api.track_getsimilar( artist = self.artist.name, track = self.name, **kargs )
        else:
            return self._api.track_getsimilar( artist = self.artist, track = self.name, **kargs )

    def gettoptags( self, **kargs ):
        if hasattr( self.artist, 'name' ):
            return self._api.track_gettags( artist = self.artist.name, track = self.name, **kargs )
        else:
            return self._api.track_gettags( artist = self.artist, track = self.name, **kargs )

    def topfans( self, **kargs ):
        if hasattr( self.artist, 'name' ):
            return self._api.track_gettopfans( artist = self.artist.name, track = self.name, **kargs )
        else:
            return self._api.track_gettopfans( artist = self.artist, track = self.name, **kargs )

    def toptags( self, **kargs ):
        if hasattr( self.artist, 'name' ):
            return self._api.track_gettoptags( artist = self.artist.name, track = self.name, **kargs )
        else:
            return self._api.track_gettoptags( artist = self.artist, track = self.name, **kargs )

    def love( self, **kargs ):
        if hasattr( self.artist, 'name' ):
            return self._api.track_love( artist = self.artist.name, track = self.name, **kargs )
        else:
            return self._api.track_love
    def removetag( self, **kargs ):
        if hasattr( self.artist, 'name' ):
            return self._api.track_removetag( artist = self.artist.name, track = self.name, **kargs )
        else:
            return self._api.track_removetag( artist = self.artist, track = self.name, **kargs )

    def scrobble( self, **kargs ):
        return self._api.track_scrobble( **kargs )

    def search( self, **kargs ):
        if hasattr( self.artist, 'name' ):
            return self._api.track_search( artist = self.artist.name, track = self.name, **kargs )
        else:
            return self._api.track_search( artist = self.artist, track = self.name, **kargs )

    def share( self, **kargs ):
        if hasattr( self.artist, 'name' ):
            return self._api.track_share( artist = self.artist.name, track = self.name, **kargs )
        else:
            return self._api.track_share( artist = self.artist, track = self.name, **kargs )

    def unban( self, **kargs ):
        if hasattr( self.artist, 'name' ):
            return self._api.track_unban( artist = self.artist.name, track = self.name, **kargs )
        else:
            return self._api.track_unban( artist = self.artist, track = self.name, **kargs )

    def unlove( self, **kargs ):
        if hasattr( self.artist, 'name' ):
            return self._api.track_unlove( artist = self.artist.name, track = self.name, **kargs )
        else:
            return self._api.track_unlove( artist = self.artist, track = self.name, **kargs )

    def updatenowplaying( self, **kargs ):
        if hasattr( self.artist, 'name' ):
            return self._api.track_updatenowplaying( artist = self.artist.name, track = self.name, **kargs )
        else:
            return self._api.track_updatenowplaying( artist = self.artist, track = self.name, **kargs )

class Tag( Model ):

    def info( self, **kargs ):
        return self._api.tag_getinfo( tag = self.name, **kargs )

    def similar( self, **kargs ):
        return self._api.tag_getsimilar( tag = self.name, **kargs )

    def topalbums( self, **kargs ):
        return self._api.tag_gettopalbums( tag = self.name, **kargs )

    def topartists( self, **kargs ):
        return self._api.tag_gettopartists( tag = self.name, **kargs )

    def toptags( self, **kargs ):
        return self._api.tag_gettoptags( **kargs )

    def toptracks( self, **kargs ):
        return self._api.tag_gettoptracks( tag = self.name, **kargs )

    def weeklyartistchart( self, **kargs ):
        return self._api.tag_getweeklyartistchart( tag = self.name, **kargs )

    def weeklychartlist( self, **kargs ):
        return self._api.tag_getweeklychartlist( tag = self.name, **kargs )

    def search( self, **kargs ):
        return self._api.tag_search( tag = self.name, **kargs )


class Search( Model ):

    members = {
        'opensearch:Query' : 'query',
        'opensearch:totalResults' : 'total_results',
        'opensearch:startIndex' : 'start_index',
        'opensearch:itemsPerPage' : 'items_per_page',
    }

class Event( Model ):

    def attend( self, **kargs ):
        return self._api.event_attend( event = self.id ** kargs )

    def attendees( self, **kargs ):
        return self._api.event_getattendees( event = self.id ** kargs )

    def info( self, **kargs ):
        return self._api.event_getinfo( event = self.id ** kargs )

    def shouts( self, **kargs ):
        return self._api.event_getshouts( event = self.id ** kargs )

    def share( self, **kargs ):
        return self._api.event_share( event = self.id ** kargs )

    def shout( self, **kargs ):
        return self._api.event_shout( event = self.id ** kargs )

class Venue( Model ):

    def events( self, **kargs ):
        return self._api.venue_getevents( venue = self.id, **kargs )

    def pastevents( self, **kargs ):
        return self._api.venue_getpastevents( venue = self.id, **kargs )

    def search( self, **kargs ):
        return self._api.venue_search( **kargs )

class Size( Model ):

    members = {
        'text' : 'url'
    }

class List( Model, list ):
    members = {
        'artist' : 'artists',
        'album' : 'albums',
        'track' : 'tracks',
        'event' : 'events',
        'venue' : 'venues',
        'tag' : 'tags',
        'chart' : 'charts',
        'user' : 'users',
    }

class Shout( Model ):
    pass

class Station( Model ):
    pass

class Geo( Model ):

    def events( self, **kargs ):
        return self._api.geo_getevents( **kargs )

    def metroartistchart( self, **kargs ):
        return self._api.geo_getmetroartistchart( **kargs )

    def metrohypeartistchart( self, **kargs ):
        return self._api.geo_getmetrohypeartistchart( **kargs )

    def metrohypetrackchart( self, **kargs ):
        return self._api.geo_getmetrohypetrackchart( **kargs )

    def metrotrackchart( self, **kargs ):
        return self._api.geo_getmetrotrackchart( **kargs )

    def metrouniqueartistchart( self, **kargs ):
        return self._api.geo_getmetrouniqueartistchart( **kargs )

    def metrouniquetrackchart( self, **kargs ):
        return self._api.geo_getmetrouniquetrackchart( **kargs )

    def metroweeklychartlist( self, **kargs ):
        return self._api.geo_getmetroweeklychartlist( **kargs )

    def metros( self, **kargs ):
        return self._api.geo_getmetros( **kargs )

    def topartists( self, **kargs ):
        return self._api.geo_gettopartists( **kargs )

    def toptracks( self, **kargs ):
        return self._api.geo_gettoptracks( **kargs )

class Group( Model ):

    def __init__( self, group, api = None ):
        self.group = group
        self._api = api

    def hype( self, **kargs ):
        return self._api.group_gethype( group = self.group, **kargs )

    def members( self, **kargs ):
        return self._api.group_getmembers( group = self.group, **kargs )

    def weeklyalbumchart( self, **kargs ):
        return self._api.group_getweeklyalbumchart( group = self.group, **kargs )

    def weeklyartistchart( self, **kargs ):
        return self._api.group_getweeklyartistchart( group = self.group, **kargs )

    def weeklychartlist( self, **kargs ):
        return self._api.group_getweeklychartlist( group = self.group, **kargs )

    def weeklytrackchart( self, **kargs ):
        return self._api.group_getweeklytrackchart( group = self.group, **kargs )

class PlayList( Model ):

    def addtrack( self, **kargs ):
        return self._api.playlist_addtrack( **kargs )

    def create( self, **kargs ):
        return self._api.playlist_create( **kargs )

class Tasteometer( Model ):

    def compare( self, **kargs ):
        return self._api.tasteometer_compare( **kargs )

    def comparegroup( self, **kargs ):
        return self._api.tasteometer_comparegroup( **kargs )

class ModelFactory( object ):

    user = User
    image = Image
    chart = Chart
    album = Album
    artist = Artist
    track = Track
    tag = Tag
    weeklychartlist = Chart
    similar = Artist
    event = Event
    venue = Venue
    images = Image
    shout = Shout
    station = Station


