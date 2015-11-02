import unittest

from werkzeug.wrappers import Request
from rpc_the.pipes.base import PipeLine
from rpc_the.pipes.json_rpc import JsonRpc2PipeIn, JsonRpc2PipeOut
from rpc_the.pipes.werkzeug import SimpleWerkzeugPipeIn, SimpleWerkzeugPipeOut
from tests.base import DEFAULT_WSGI_ENVIRON, DummyPipe


class JsonRpcTestCase(unittest.TestCase):

    def setUp(self):
        self.default_request = Request(DEFAULT_WSGI_ENVIRON)
        self.default_request.data = '{"method": "test", "params": [1]}'

    def test_basic(self):
        message = 'Hello World!'
        pipeline = PipeLine\
            ( SimpleWerkzeugPipeIn()
            , JsonRpc2PipeIn()
            , DummyPipe(message=message)
            , JsonRpc2PipeOut()
            , SimpleWerkzeugPipeOut()
            )

        result = pipeline(self.default_request)

        self.assertEqual(result.data, message)

    # def test_excepetion(self):
    #     pipeline = PipeLine\
    #         ( SimpleWerkzeugPipeIn()
    #         , DummyPipe
    #           ( raises_error=True
    #           , message='ERROR'
    #           )
    #         , SimpleWerkzeugPipeOut()
    #         )
    #
    #     result = pipeline(self.default_request)
    #
    #     self.assertEqual(result.data, 'ERROR')
    #     self.assertEqual(result.status_code, 500)