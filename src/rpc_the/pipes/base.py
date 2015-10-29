import traceback
from rpc_the.utils import apply_settings, ImmutableSettings


class PipeLine(object):

    def __init__(self, *pipeline):
        for handler in pipeline:
            if not callable(handler) and not callable(getattr(handler, 'handle_exception', None)):
                raise ValueError('%s is not a "Pipe" object' % repr(handler))
        self._pipeline = pipeline

    def __call__(self, *args, **kwargs):
        exception = None
        for handler in self._pipeline:
            try:
                if exception:
                    exception, args, kwargs = handler.handle_exception(exception, *args, **kwargs)
                    continue
                args, kwargs = handler(*args, **kwargs)
            except Exception as exception:
                print traceback.print_exc()
                print type(exception), exception
                continue
        return args, kwargs


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

    def __call__(self, *args, **kwargs):
        return self.handle(*args, **kwargs)

    def handle_exception(self, exception, *args, **kwargs):
        """
        @param exception:
        @param args:
        @param kwargs:
        @return: raise Exception or returns tuple (exception, args, kwargs)
        """
        # Transfer control to next pipe by default
        raise exception

    def handle(self, *args, **kwargs):
        raise NotImplementedError('BasePipe.handle must be implemented')
