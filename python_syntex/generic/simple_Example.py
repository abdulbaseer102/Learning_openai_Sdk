# 1. Why Use Generics?

# Let's consider an example without generics:


# def double_number(n: int) -> int:
#    return n * 2
#print(double_number(5))   # ✅ Works fine
#print(double_number(5.5)) # ❌ Type error (expected int)



#def double_number(n: int) -> int:
 #   return n * 2

#print(double_number(5))   # ✅ Works fine
#print(double_number(5.5)) # ❌ Type error (expected int)



# 2. Basic Syntax of Generics (TypeVar)

# Generics in Python are implemented using TypeVar from typing.

# from typing import TypeVar

# T = TypeVar("T")  # T represents a generic type

# T is a placeholder that can be replaced with any type when the function is called.
# The actual type is inferred at runtime.


# 3. Using Generics in Function

# from typing import TypeVar

# T = TypeVar("T")  # Generic Type

#def identity(value: T) -> T:
 #   return value

# print(identity(5))        # ✅ Works with int
# print(identity("Hello"))  # ✅ Works with str
# print(identity([1, 2, 3])) # ✅ Works with list*\



# How It Works:

# T is a type variable, meaning that whatever type we pass, the function adapts.
# identity(5) → T becomes int
# identity("Hello") → T becomes str
# identity([1, 2, 3]) → T becomes list[int]


from typing import TypeVar

T = TypeVar("T")  # Generic Type

def identity(value: T) -> T:
    return value

print(identity(5))        # ✅ Works with int
print(identity("Hello"))  # ✅ Works with str
print(identity([1, 2, 3])) # ✅ Works with list