from logging import getLogger

__all__ = ['AutoGetlogger', 'auto_getlogger']


class AutoGetLoggerType(type):
    """
    Wrap all methods so that they are passed an l parameter that is a logger initialized using getLogger('Class.method')
    """

    def __new__(mcs, name, bases, dictionary):
        for k, v in dictionary.items():
            if 'function' == v.__class__.__name__:
                dictionary[k] = mcs.add_logger_to_method(dictionary[k], name)
            elif 'staticmethod' == v.__class__.__name__:
                dictionary[k] = mcs.add_logger_to_staticmethod(dictionary[k], name)
            elif 'classmethod' == v.__class__.__name__:
                dictionary[k] = mcs.add_logger_to_classmethod(dictionary[k], name)
        return type.__new__(mcs, name, bases, dictionary)

    @classmethod
    def add_logger_to_method(mcs, method_reference, name):

        def wrapper(self, *args, **kwargs):
            # TODO: If I use instead self.__class__.__name__ does that lead to more correct results WRT inheritance?
            # Or is name just as correct?
            logger = getLogger('{0}.{1}'.format(name, method_reference.__name__))
            return method_reference(self, *args, l=logger, **kwargs)
        return wrapper

    @classmethod
    def add_logger_to_staticmethod(mcs, method_reference, name):

        def wrapper(*args, **kwargs):
            logger = getLogger('{0}.{1}'.format(name, method_reference.__name__))
            return method_reference(*args, l=logger, **kwargs)
        return wrapper

    @classmethod
    def add_logger_to_classmethod(mcs, method_reference, name):

        def wrapper(cls, *args, **kwargs):
            logger = getLogger('{0}.{1}'.format(name, method_reference.__name__))
            return method_reference(cls, *args, l=logger, **kwargs)
        return wrapper


class AutoGetLogger(object):
    __metaclass__ = AutoGetLoggerType


def auto_getlogger(method_reference):
    def wrapper(*args, **kwargs):
        logger = getLogger(method_reference.__name__)
        return method_reference(*args, l=logger, **kwargs)
    return wrapper
