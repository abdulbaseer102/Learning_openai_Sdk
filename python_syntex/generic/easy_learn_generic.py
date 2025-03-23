# 1. Introduction to Generics

# Example without Generics
def first_element(items):
    """
    Takes a list...

    Args:
      items: A list of items.

    Returns:
      The first item in the list.
    """
    return items[0]

nums = [1,2,3]
string =["a","b","c"]


# print(first_element(nums))
# print(first_element(string))

# Issue: No type checking. We can't restrict or inform about expected data types explicitly.

# 2. Using Generics

# Generics let you create functions, methods, or classes that can work with multiple types while preserving type relationships. Generics:

# . Better communicate the intent of your code.
# . Allow static type checking to verify correctness.

# . In Python, this is done using TypeVar.

# 🔹 Using TypeVar First, import TypeVar and define a generic type variable T:
from typing import TypeVar

T = TypeVar("T") # T represents a generic type

# T is a placeholder that can be replaced with any type when the function is called.
# The actual type is inferred at runtime.

# Type variable for generic typing
from typing import TypeVar

# Analogy -> Think of T as fill in the Blank
# -> using T is community driven practice.
T = TypeVar('T')

def generic_first_element(items: list[T]) -> T:
    return items[0]

num_result = generic_first_element(nums)            # type inferred as int
string_result = generic_first_element(string)       # type inferred as str    


print(num_result)     # 1
print(string_result)  # a

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Why Use Generics When Python Lets You Pass Any List? see here --> python_syntex/generics_in_python.py/readme.md

# Dictionary example using two generic types (K and V):

from typing import TypeVar

K = TypeVar('K') # Keys
V = TypeVar('V') # Values

def get_item(container: dict[K, V], key: K) -> V:
    return container[key]

# Here, it’s clear that:
    # . The key must match the dictionary key type (K).
    # . The returned value is always the type of dictionary’s values (V).

# Using this    
d = {'a': 1, 'b': 2}

value = get_item(d, 'a')  # returns int
print(value)




# 3. Generic Classes
from typing import Generic, TypeVar, ClassVar
from dataclasses import dataclass, field

# Type variable for generic typing
T = TypeVar('T')

@dataclass
class Stack(Generic[T]):
    # Instance Level -> obj = Stack
    items: list[T] = field(default_factory=list)
    # Class Level ->
    limit: ClassVar[int] = 10

    def push(self, item:T) -> None:
        self.items.append(item)

    def pop(self) -> T:
        return self.items.pop()

# Infer
# 1. On seeing T i assumed there will be generic types.
# 2. T is an unknown/ fill in the blank type. We will get type in runtime.
# 
stack_of_ints = Stack[int]()
print(stack_of_ints)        


print(stack_of_ints)
print(stack_of_ints.limit)

stack_of_ints.push(10)
stack_of_ints.push(20)
stack_of_ints


print(stack_of_ints.pop())  # 20


stack_of_strings = Stack[str]()
print(stack_of_strings)

stack_of_strings.push("hello")
stack_of_strings.push("world")

print(stack_of_strings.pop())  # 'world'

print(Stack.limit)
print(stack_of_ints.limit)







# Advanced Usage of Generics

# Using Generics with multiple TypeVars

from dataclasses import dataclass
from typing import TypeVar

K = TypeVar('K')
V = TypeVar('V')

# Incorrect Usage (without Generic inheritance)
@dataclass
class KeyValuePair:
    key: K
    value: V
# This snippet incorrectly attempts generics without inheriting from Generic, causing static type checkers to complain.

pair = KeyValuePair("age", 30)

print(pair.key,pair.value)    # 'age'
print(pair.value)  # 30




# Correct Usage (with Generic inheritance)
@dataclass
class CorrectKeyValuePair(Generic[K, V]):
    key: K
    value: V

pair = CorrectKeyValuePair("age", 30)

print(pair.key)    # 'age'
print(pair.value)  # 30



# Explanation of Differences:

# Without Generic inheritance: TypeVars K, V are unbound, causing static checkers to fail.
# With Generic inheritance: Explicitly informs type checkers, ensuring accurate type inference and improved static checking.


# Practical Example with Generics

# a. Generic function that merges two dictionaries

def merge_dicts(dict1: dict[K, V], dict2: dict[K, V]) -> dict[K, V]:
    result = dict1.copy()
    result.update(dict2)
    return result

merged = merge_dicts({'a': 1}, {'b': 2})
print(merged)  # {'a': 1, 'b': 2}




# b. Generics with DataClasses

# Dataclasses combined with Generics enhance clarity, immutability, and type safety for complex data structures.

@dataclass
class GenericDataContainer(Generic[T]):
    data: T

int_container = GenericDataContainer[int](data=123)
str_container = GenericDataContainer[str](data="Generics in Python")

print(int_container.data)  # 123
print(str_container.data)  # 'Generics in Python'





# Production Grade Example for AI Agents
@dataclass
class AgentState(Generic[K, V]):
    context: dict[K, V]
    status: str

agent_state = AgentState[str, str](context={"task": "data collection", "priority": "high"}, status="active")

print(agent_state.context)  # {'task': 'data collection', 'priority': 'high'}
print(agent_state.status)   # 'active'




# Summary

# Always explicitly inherit from Generic when using TypeVar in Python classes to clearly communicate intentions to
# static type checkers and to avoid subtle type-related bugs.

# Generics significantly enhance type safety, readability, and maintainability, making them critical for robust, 
# scalable, and production-grade AI agent systems.