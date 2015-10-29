import unittest

from rpc_the.pipes.base import Pipe, PipeLine


class C1(Pipe):

    step = 1

    defaults = \
        { 'do_raise': True
        , }

    def handle(self, *args, **kwargs):
        if self.settings.do_raise:
            raise TypeError('Error in 1')
        return (args[0] + self.step, ), kwargs


class C2(Pipe):

    step = 20

    defaults = \
        { 'do_raise': True
        , }

    def handle(self, *args, **kwargs):
        if self.settings.do_raise:
            raise ValueError('Error in 2')
        return (args[0] + self.step, ), kwargs

    def handle_exception(self, exception, *args, **kwargs):
        i = args[0]
        try:
            raise exception
        except TypeError:
            i += (self.step ** 2)
        args, kwargs = self.handle(i, **kwargs)
        return None, args, kwargs


class C3(Pipe):

    step = 30

    def handle(self, *args, **kwargs):
        return (self.step + args[0], ), kwargs

    def handle_exception(self, exception, *args, **kwargs):
        i = args[0]
        try:
            raise exception
        except ValueError:
            i += (self.step ** 2)
        args, kwargs = self.handle(i, **kwargs)
        return None, args, kwargs


class TestPipeTestCase(unittest.TestCase):

    def test_basic(self):
        args, kwargs = PipeLine(C1(), C2(), C3())(1)
        self.assertEqual((931, ), args)

        args, kwargs = PipeLine(C1(do_raise=False), C2(), C3())(1)
        self.assertEqual((932, ), args)

        args, kwargs = PipeLine(C1(do_raise=False), C2(do_raise=False), C3())(1)
        self.assertEqual((52, ), args)
