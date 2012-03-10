import time
import threading
import logging

logger = logging.getLogger( 'lastvis.custom' )

class RateController( object ):

    def __init__( self, query_interval = None ):

        if query_interval is None:
            queries_per_second = 5
            query_interval = 1 / float( queries_per_second )

        self.rate_control = { 'wait': query_interval,
                                'earliest' : None,
                                'timer' : None }
        self.control_rate()

    def control_rate( self, monitor = None ):

        if monitor is None:
            monitor = self.rate_control

        if monitor['timer'] is not None:
            monitor['timer'].join()

            while time.time() < monitor['earliest']:
                logger.info( 'LOGGER: pausing *********' )
                time.sleep( monitor['earliest'] - time.time() )

        earliest = time.time() + monitor['wait']
        timer = threading.Timer( earliest - time.time(), lambda: None )
        monitor['earliest'] = earliest
        monitor['timer'] = timer
        monitor['timer'].start()
