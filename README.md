auto_getlogger
================

All methods should start by saying l = getLogger('MyClass.my_method'). Let's make that easy!

Example
-------

```python
from auto_getlogger import AutoGetLogger

class ExampleClass(AutoGetLogger):

    def example_method(self, l, foo, bar):
        l.debug('called with foo: %r, bar: %r', foo, bar)
```

Limitations
-----------

Currently doesn't work with either static or class methods.
I'm not sure how to solve this problem. I'm working on it thought.
