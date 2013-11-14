from logging import getLogger
from types import FunctionType

__all__ = ['AutoGetlogger']


class AutoGetLoggerType(type):
    """
    Wrap all methods so that they are passed an l parameter that is a logger initialized using getLogger('Class.method')
    """

    def __new__(mcs, name, bases, dictionary):
        for k, v in dictionary.items():
            if isinstance(v, FunctionType):
                dictionary[k] = mcs.add_logger(dictionary[k])
        return type.__new__(mcs, name, bases, dictionary)

    @classmethod
    def add_logger(mcs, method_reference):

        def wrapper(self, *args, **kwargs):
            logger = getLogger('{0}.{1}'.format(self.__class__.__name__, method_reference.__name__))
            return method_reference(self, *args, l=logger, **kwargs)
        return wrapper


class AutoGetLogger(object):
    __metaclass__ = AutoGetLoggerType
