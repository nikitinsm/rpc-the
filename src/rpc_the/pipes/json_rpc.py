import json

from rpc_the.pipes.base import Pipe


class JsonRpc2PipeIn(Pipe):

    def handle(self, message):
        envelope = json.loads(message.data)

        method = envelope['method']
        params = envelope['params']

        message.method = method
        message.data = params

        return message


class JsonRpc2PipeOut(Pipe):

    def handle(self, message):
        envelope = \
            { 'id': 0
            , 'result': message.data
            }
        message.data = json.dumps(envelope)
        return message

    def handle_exception(self, message):
        try:
            raise message.exception
        except Exception as exception:
            message.data = \
                { 'id': 0
                , 'error':
                  { 'code': getattr(exception, 'code', -32000)
                  , 'message': exception.message
                } }
        return message