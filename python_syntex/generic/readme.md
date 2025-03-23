# Using Generics in Python

Generics in Python allow you to write flexible and reusable code that can work with different data types while maintaining type safety. By using generics, you can define functions, classes, and methods that operate on a variety of types without specifying the exact type until the code is used. This is achieved through the `typing` module, which provides tools like `TypeVar` and `Generic` for type hinting.

## Why Use Generics?

- **Reusability**: Write code once and use it with multiple types.
- **Type Safety**: Catch type-related errors at compile time using tools like `mypy`.
- **Flexibility**: Build versatile libraries that support various data types.

Below are four examples demonstrating different ways to use generics in Python. Each example is provided in a separate file for clarity and modularity.

---

## Example 1: Generic Function

A generic function can operate on different types. The following function returns the first element of a list, regardless of the type of elements in the list.

```python
from typing import TypeVar, List

T = TypeVar('T')

def first_element(lst: List[T]) -> T:
    return lst[0]

