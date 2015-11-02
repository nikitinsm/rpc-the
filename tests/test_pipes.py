import unittest

from rpc_the.pipes.base import Pipe, PipeLine, PipeMessage


class C1(Pipe):

    step = 1

    defaults = \
        { 'do_raise': True
        , }

    def handle(self, message):
        if self.settings.do_raise:
            raise TypeError('Error in 1')
        message.i += self.step
        return message


class C2(Pipe):

    step = 20

    defaults = \
        { 'do_raise': True
        , }

    def handle(self, message):
        if self.settings.do_raise:
            raise ValueError('Error in 2')
        message.i += self.step
        return message

    def handle_exception(self, message):
        try:
            raise message.exception
        except TypeError:
            message.i += (self.step ** 2)
        return message


class C3(Pipe):

    step = 30

    def handle(self, message):
        message.i += self.step
        return message

    def handle_exception(self, message):
        try:
            raise message.exception
        except ValueError:
            message.i += (self.step ** 2)
        message = self.handle(message)
        return message


class PipeTestCase(unittest.TestCase):

    def test_basic(self):
        message = PipeMessage()
        message.i = 0
        message = PipeLine(C1(), C2(), C3())(message)
        self.assertEqual(message.i, 430)

        message = PipeMessage()
        message.i = 0
        message = PipeLine(C1(do_raise=False), C2(), C3())(message)
        self.assertEqual(message.i, 931)

        message = PipeMessage()
        message.i = 0
        message = PipeLine(C1(do_raise=False), C2(do_raise=False), C3())(message)
        self.assertEqual(message.i, 51)
