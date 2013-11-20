auto_getlogger
================

All methods should start by saying l = getLogger('MyClass.my_method'). Let's make that easy!

Usage
-----

```python
>>> from logging import basicConfig
>>> basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s')
>>> from auto_getlogger import *
>>> @auto_getlogger
... def example_function(l, foo=None):
...     l.error('foo: %r', foo)
...
>>>
>>> example_function(foo='bar')
2013-11-19 17:38:57,969 example_function ERROR foo: 'bar'
>>> class ExampleClass(AutoGetLogger):
...     def example_method(self, l, foo=None):
...         l.error('called with foo: %r', foo)
...
>>> class InheritedExample(ExampleClass):
...     pass
...
>>> i = InheritedExample()
>>> i.example_method(foo='bar')
2013-11-19 18:11:41,877 InheritedExample.example_method ERROR called with foo: 'bar'
```

Limitations
-----------

Currently doesn't work with either static or class methods.
I'm not sure how to solve this problem. I'm working on it thought.
