from auto_getlogger import AutoGetLogger, auto_getlogger
from unittest2 import TestCase


class T(AutoGetLogger):
    def regular_method(*args, **kwargs):
        return args, kwargs

    @property
    def my_property(*args, **kwargs):
        return args, kwargs

    @staticmethod
    def static_method(*args, **kwargs):
        return args, kwargs

    @classmethod
    def class_method(*args, **kwargs):
        return args, kwargs


class U(T):
    pass


class TestAutoGetLogger(TestCase):

    def test_regular_method(self):
        t = T()
        args, kwargs = t.regular_method()
        self.assertEqual(1, len(args))
        self.assertEqual(t, args[0])
        self.assertEqual(1, len(kwargs))
        self.assertItemsEqual(('l',), kwargs.keys())
        l = kwargs['l']
        self.assertEqual('Logger', l.__class__.__name__)
        self.assertEqual('T.regular_method', l.name)

    def test_property(self):
        t = T()
        args, kwargs = t.my_property
        self.assertEqual(1, len(args))
        self.assertEqual(t, args[0])
        self.assertEqual(1, len(kwargs))
        self.assertItemsEqual(('l',), kwargs.keys())
        l = kwargs['l']
        self.assertEqual('Logger', l.__class__.__name__)
        self.assertEqual('T.my_property', l.name)

    def test_static_method(self):
        args, kwargs = T.static_method()
        self.assertEqual(0, len(args))
        self.assertEqual(1, len(kwargs))
        self.assertItemsEqual(('l',), kwargs.keys())
        l = kwargs['l']
        self.assertEqual('Logger', l.__class__.__name__)
        self.assertEqual('T.static_method', l.name)

    def test_class_method(self):
        args, kwargs = T.class_method()
        self.assertEqual(1, len(args))
        self.assertEqual(T, args[0])
        self.assertEqual(1, len(kwargs))
        self.assertItemsEqual(('l',), kwargs.keys())
        l = kwargs['l']
        self.assertEqual('Logger', l.__class__.__name__)
        self.assertEqual('T.class_method', l.name)

    def test_inheritance(self):
        t = U()
        args, kwargs = t.regular_method()
        self.assertEqual(1, len(args))
        self.assertEqual(t, args[0])
        self.assertEqual(1, len(kwargs))
        self.assertItemsEqual(('l',), kwargs.keys())
        l = kwargs['l']
        self.assertEqual('Logger', l.__class__.__name__)
        self.assertEqual('U.regular_method', l.name)


class TestAutoGetLoggerFunction(TestCase):

    def test_a(self):
        @auto_getlogger
        def fake_method(l):
            return l
        t = fake_method()
        self.assertEqual('Logger', t.__class__.__name__)
        self.assertEqual('fake_method', t.name)
