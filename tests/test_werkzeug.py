import unittest

from werkzeug.wrappers import Request
from rpc_the.pipes.base import Pipe, PipeLine
from rpc_the.pipes.werkzeug import SimpleWerkzeugPipeIn, SimpleWerkzeugPipeOut
from tests.base import DEFAULT_WSGI_ENVIRON


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


class WerkzeugTestCase(unittest.TestCase):

    def setUp(self):
        self.default_request = Request(DEFAULT_WSGI_ENVIRON)

    def test_basic(self):
        message = 'Hello World!'
        pipeline = PipeLine\
            ( SimpleWerkzeugPipeIn()
            , DummyPipe(message=message)
            , SimpleWerkzeugPipeOut()
            )

        result = pipeline(self.default_request)

        self.assertEqual(result.data, message)

    def test_excepetion(self):
        pipeline = PipeLine\
            ( SimpleWerkzeugPipeIn()
            , DummyPipe(raises_error=True, message='ERROR')
            , SimpleWerkzeugPipeOut()
            )

        result = pipeline(self.default_request)

        self.assertEqual(result.data, 'ERROR')
        self.assertEqual(result.status_code, 500)



