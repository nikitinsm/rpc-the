import traceback

from rpc_the.utils import ImmutableDict
from rpc_the.utils import apply_settings, ImmutableSettings


class PipeLine(object):

    def __init__(self, *pipeline):
        for handler in pipeline:
            if not callable(handler) and not callable(getattr(handler, 'handle_exception', None)):
                raise ValueError('%s is not a "Pipe" object' % repr(handler))
        self._pipeline = pipeline

    def __call__(self, message):
        for handler in self._pipeline:
            try:
                message = handler(message)
            except Exception as exception:
                message.exception = exception
                # print traceback.print_exc()
                # print type(exception), exception
                continue
        return message


class Pipe(object):

    defaults = None
    settings = None

    def __init__(self, **settings):
        settings = apply_settings\
            ( self.__class__
            , self.defaults or {}
            , settings
            )
        self.settings = ImmutableSettings(**settings)

    def __call__(self, message):
        if issubclass(type(getattr(message, 'exception', None)), Exception):
            result = self.handle_exception(message)
            setattr(message, 'exception', None)
            return result
        return self.handle(message)

    def handle(self, message):
        raise NotImplementedError('BasePipe.handle must be implemented')

    def handle_exception(self, message):
        """
        @param exception:
        @param message:
        @raise Exception
        @return: PipeMessage
        """
        # Transfer control to next pipe by PipeMessage
        raise message.exception


class PipeMessage(object):
    exception = None


# class BaseAdapter(object):
#
#     required = None
#     optional = None
#
#     def __init__(self, **kwargs):
#         self.__dict__ = ImmutableDict(**kwargs)
#
#
# class HttpRequestAdapter(BaseAdapter):
#
#     def __init__(self, method, header, body=None, path=None, args=None):
#         kwargs = locals()
#         kwargs.pop('self')
#         super(HttpRequestAdapter, self).__init__(**kwargs)
