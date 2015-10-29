import copy
from itertools import repeat
from six import iteritems


def is_immutable(self):
    raise TypeError('%r objects are immutable' % self.__class__.__name__)


class ImmutableDictMixin(object):
    _hash_cache = None

    @classmethod
    def fromkeys(cls, keys, value=None):
        instance = super(cls, cls).__new__(cls)
        instance.__init__(zip(keys, repeat(value)))
        return instance

    def __reduce_ex__(self, protocol):
        return type(self), (dict(self),)

    def _iter_hashitems(self):
        return iteritems(self)

    def __hash__(self):
        if self._hash_cache is not None:
            return self._hash_cache
        rv = self._hash_cache = hash(frozenset(self._iter_hashitems()))
        return rv

    def setdefault(self, key, default=None):
        is_immutable(self)

    def update(self, *args, **kwargs):
        is_immutable(self)

    def pop(self, key, default=None):
        is_immutable(self)

    def popitem(self):
        is_immutable(self)

    def __setitem__(self, key, value):
        is_immutable(self)

    def __delitem__(self, key):
        is_immutable(self)

    def clear(self):
        is_immutable(self)


class ImmutableDict(ImmutableDictMixin, dict):

    def __repr__(self):
        return '%s(%s)' % (
            self.__class__.__name__,
            dict.__repr__(self),
        )

    def copy(self):
        return dict(self)

    def __copy__(self):
        return self


class ImmutableSettings(ImmutableDict):

    def __getattr__(self, item):
        return self[item]


def apply_settings(cls, default_settings, new_settings):
    default_keys = set(default_settings.keys())
    new_keys = set(new_settings.keys())
    if not default_keys >= new_keys:
        illegal_keys = new_keys - (default_keys & new_keys)
        base_message = '"%s" is illegal setting for "%s"'
        if len(illegal_keys) > 1:
            base_message = '"%s" are illegal settings for "%s"'
        raise ValueError\
            ( base_message %
              ( ', '.join(map(str, illegal_keys))
              , cls.__name__
            ) )
    result = copy.copy(default_settings)
    result.update(new_settings)
    return result