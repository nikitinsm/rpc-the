import collections


class JsonDocument(collections.MutableMapping):

    data = None

    def __init__(self, **data):
        self.data = data

    def __getitem__(self, key):
        return self.data[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        self.data[self.__keytransform__(key)] = value

    def __delitem__(self, key):
        del self.data[self.__keytransform__(key)]

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __keytransform__(self, key):
        return key

    # def to_json(self):
    #     return settings.serializer(self.data)
    #
    # @classmethod
    # def from_json(cls, data):
    #     return cls(settings.deserializer(data))
