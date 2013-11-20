auto_getlogger
================

`auto_getlogger` provides a consistently initialized logger in every context with minimal code change.

Rationale
---------

One of the great strengths of modern logging systems is category logging.
To get the most from category logging, your code needs to follow a
consistent schema when it allocates loggers.
There are plenty of reasonable options for such a schema, but more important than
which schema you choose is the consistency of it's application.
This code implements a ClassName.method_name schema.

Usage
-----

```python
>>> # Configure logging so we can see the messages we are about to generate.
>>> from logging import basicConfig
>>> basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s')
>>>
>>> # Actual example code starts here.
>>> from auto_getlogger import *
>>> @auto_getlogger
... def example_function(l, foo=None):
...     l.error('foo: %r', foo)
...
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

As you can see from the two failing tests,
this module currently doesn't work with either static or class methods.
I'm not sure how to solve this problem. I'm working on it though.

Migrating Legacy Code
---------------------

This is where `auto_getlogger` really shines. It takes 6 steps.

1. Replace importing direct calls to `debug`, `info`, etc. with the import of `auto_getlogger`.
1. For all classes, include `AutoGetLogger` in their interitance tree.
1. For all functions, wrap them with `@auto_getlogger`.
1. Make sure you are not using `l` as a local variable name or formal parameter elsewhere in the code.
1. For all function and method calls, add the formal parameter `l` as a first keyword argument.
1. For all cases where you have (now broken) direct calls to `debug`, `info`, etc. prepend an `l.`
   so that they  are calling through the provided logger object.

The following diff demonstrates the upgrade of some legacy code to use `auto_getlogger`.

```diff
-from logging import debug, info, warning, error, exception
+from auto_getlogger import *

+class LegacyClass(AutoGetLogger):

-class LegacyClass(object):
+    def legacy_method(self, foo, l, bar=None):
+        l.warning('legacy_method self: %r, foo: %r, bar: %r', self, foo, bar)

-    def legacy_method(self, foo, bar=None):
-        warning('legacy_method self: %r, foo: %r, bar: %r', self, foo, bar)

-
-def legacy_function(foo, bar=None):
-    error('legacy_function foo: %r, bar: %r', foo, bar)
+@auto_getlogger
+def legacy_function(foo, l, bar=None):
+    l.error('legacy_function foo: %r, bar: %r', foo, bar)
```
