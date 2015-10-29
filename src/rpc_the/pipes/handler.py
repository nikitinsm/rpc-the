import re

from rpc_the.utils import ImmutableSettings, apply_settings


METHOD_NAME_RE = re.compile(r'^[A-Za-z]+[A-Za-z0-9_-]*[A-Za-z0-9]$')


class CallableHandler(object):

    _methods = None

    settings = None
    defaults = \
        { 'takes_parent': True
        , }

    def __init__(self, *methods, **settings):
        self._methods = dict()

        # Prepare settings
        settings = apply_settings\
            ( self.__class__
            , self.defaults
            , settings
            )
        self.settings = ImmutableSettings(**settings)

        # Prepare methods
        for method in methods:
            self.add_method(method.__name__, method)

    def __setitem__(self, name, value):
        return self.add_method(name, value)

    def __getitem__(self, name):
        return self.get_method(name)

    def add_method(self, name, f, **settings):
        if not METHOD_NAME_RE.match(name):
            raise ValueError('%s: invalid method name' % self.__class__.__name__)

        if not callable(f):
            raise ValueError('%s: invalid callable' % self.__class__.__name__)

        # Prepare settings
        settings = apply_settings\
            ( f
            , self.settings or {}
            , settings
            )
        self._methods[name] = (f, ImmutableSettings(**settings))

    def get_method(self, name):
        method_callable, method_settings = self._methods[name]
        return method_callable

    def __call__(self, parent, name, *args, **kwargs):
        callable_object, method_settings = self.get_method(name)
        if method_settings['takes_parent'] is True:
            args = (parent, ) + args
        return callable_object(*args, **kwargs)


def method(service, name=None, **settings):

    def decorator(f):
        service.add_method\
            ( name or f.__name__
            , f
            , **settings
            )
        return f
    return decorator


default_handler = CallableHandler()
