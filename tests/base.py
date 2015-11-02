import os
import sys
from rpc_the.pipes.base import Pipe


DEFAULT_WSGI_ENVIRON = dict(os.environ.items())
DEFAULT_WSGI_ENVIRON.update\
    ( { 'wsgi.input': sys.stdin
      , 'wsgi.errors': sys.stderr
      , 'wsgi.version': (1, 0)
      , 'wsgi.multithread': False
      , 'wsgi.multiprocess': True
      , 'wsgi.run_once': True
      , 'wsgi.url_scheme': 'http'
    } )


class DummyPipe(Pipe):

    defaults = \
        { 'message': None
        , 'raises_error': False
        }

    def handle(self, message):
        message.data = self.settings.message
        if self.settings.raises_error:
            raise Exception('simple error')

        return message