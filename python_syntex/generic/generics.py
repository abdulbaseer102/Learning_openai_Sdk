# Using Generics in Functions

from typing import TypeVar

T = TypeVar("T")  # Generic Type

def identity(value: T) -> T:
    return value

print(identity(5))        # ✅ Works with int
print(identity("Hello"))  # ✅ Works with str
print(identity([1, 2, 3])) # ✅ Works with list



# Using Generics in Classes

from typing import Generic, TypeVar

T = TypeVar("T")  # Define a type variable

class Container(Generic[T]):  # Declare a generic class
    def __init__(self, value: T):
        self.value = value

    def get_value(self) -> T:
        return self.value

# Creating instances with different types
c1 = Container(10)          # T becomes int
c2 = Container("Python")    # T becomes str
c3 = Container([1, 2, 3])   # T becomes list[int]

print(c1.get_value())  # 10
print(c2.get_value())  # Python
print(c3.get_value())  # [1, 2, 3]





# Generics with Multiple Type Variables


from typing import TypeVar, Generic

K = TypeVar("K")  # Key type
V = TypeVar("V")  # Value type

class KeyValuePair(Generic[K, V]):
    def __init__(self, key: K, value: V):
        self.key = key
        self.value = value

    def get_pair(self) -> tuple[K, V]:
        return (self.key, self.value)

pair1 = KeyValuePair("id", 101)       # str, int
pair2 = KeyValuePair(1, "Python")     # int, str

print(pair1.get_pair())  # ('id', 101)
print(pair2.get_pair())  # (1, 'Python')




#  Generics with Constraints (bound=)

# Example: Restricting Generics to Numeric Types
# from typing import TypeVar

# TypeVar bound to (restricted to) float and int types
# Number = TypeVar("Number", int, float)

#def add(x: Number, y: Number) -> Number:
 #   return x + y

# print(add(3, 5))     # ✅ Works with int
# print(add(2.5, 1.2)) # ✅ Works with float
# print(add("3", "5")) # ❌ Type error: str is not allowed
# ✅ Advantage:


# Ensures only numbers are accepted (not strings, lists, etc.).


from typing import TypeVar

# TypeVar bound to (restricted to) float and int types
Number = TypeVar("Number", int, float)

def add(x: Number, y: Number) -> Number:
    return x + y

print(add(3, 5))     # ✅ Works with int
print(add(2.5, 1.2)) # ✅ Works with float
print(add("3", "5")) # ❌ Type error: str is not allowed





#  Generics with Data Structures (list[T], dict[K, V])

# Generics are often used with data structures.

# Example: Generic Stack Implementation

# ✅ Advantage:

# A Stack[int] ensures that only integers are stored.
# If you try stack_int.push("hello"), Python will raise a type error.



from typing import TypeVar, Generic

T = TypeVar("T")

class Stack(Generic[T]):
    def __init__(self):
        self.items: list[T] = []

    def push(self, item: T) -> None:
        self.items.append(item)

    def pop(self) -> T:
        return self.items.pop()

    def is_empty(self) -> bool:
        return len(self.items) == 0

stack_int = Stack[int]()
stack_int.push(10)
stack_int.push(20)

print(stack_int.pop())  # 20
print(stack_int.pop())  # 10






# 8. Generics in Function Parameters (Callable)

# Some functions accept another function as a parameter. We can use Callable with generics.

# Example: Generic Function as Parameter

# from typing import TypeVar, Callable

# T = TypeVar("T")

# def apply_function(func: Callable[[T], T], value: T) -> T:
  #  return func(value)

# def square(n: int) -> int:
  #  return n * n

# print(apply_function(square, 5))  # 25
# ✅ Advantage:

# The function adapts dynamically to different functions passed as arguments.

from typing import TypeVar, Callable

T = TypeVar("T")

def apply_function(func: Callable[[T], T], value: T) -> T:
    return func(value)

def square(n: int) -> int:
    return n * n

print(apply_function(square, 5))  # 25