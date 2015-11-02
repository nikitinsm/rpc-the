from __future__ import absolute_import

import traceback

from werkzeug.wrappers import Response, Request
from rpc_the.pipes.base import Pipe, PipeMessage


class SimpleWerkzeugPipeIn(Pipe):

    def handle(self, request):
        assert issubclass(type(request), Request)
        message = PipeMessage()

        # set Werkzeug level data
        setattr(message, self.__class__.__name__, request)

        # set common attributes
        setattr(message, 'path', request.path)

        data = request.get_data()
        if data:
            setattr(message, 'data', data)
        else:
            setattr(message, 'data', request.args)

        return message


class SimpleWerkzeugPipeOut(Pipe):

    def handle(self, message):
        return Response\
            ( message.data
            , getattr(message, 'status', 200)
            )

    def handle_exception(self, message):
        if not message.data:
            try:
                raise message.exception
            except Exception as exception:
                output = traceback.format_exc() + '\n'
                output += '-' * 10 + '\n'
                output += repr(exception) + ':' + exception.message + '\n'
                message.data = output
        print 'message', message.data
        setattr(message, 'status', 500)
        return self.handle(message)
