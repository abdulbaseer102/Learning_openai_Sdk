# 4. Callables in Python

# In Python, a callable is anything that can be “called” using (...). This most commonly refers to functions (e.g., def 
# foo(): ...), but classes (via __call__), lambdas, functools.partial objects, and so on can also be callables.

# 4.1 Basic Callable Type Hints

# To specify that a variable, parameter, or attribute is a function or callable, Python provides the Callable type hint. 

# The typical usage is:

from typing import Callable

# A callable that takes two integers and returns a string
MyFuncType = Callable[[int, int], str]


print(MyFuncType) # will print ---> typing.Callable[[int, int], str]

from dataclasses import dataclass


@dataclass
class Calculator:
    operation: Callable[[int, int], str]

    def __call__(self, a: int, b: int) -> str:
        return self.operation(a, b)
    
def add_and_stringify(x:int, y:int) -> str:
    return str(x+y)

calculation = Calculator(operation=add_and_stringify)


print(calculation(65,38))