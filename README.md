# Strict-Decorator
Decorator implements type-checking for functions via type-annotations in Python.

Works with single functions and class methods

## Usage:
```Python
@strict
def foo(a: int): pass
foo(9) #Ok

class test:
    @strict
    def foo(self, a: int): pass

t = test()
t.foo('8') #TypeError
```
