
from dataclasses import dataclass, field


@dataclass
class TruePerson:
    name: str
    _age: int
    __bank_account_balance: int = field(default=0)

    def set_bank_balance(self, balance: int):
        if balance < 0:
            raise ValueError("Balance cannot be negative.")
        self.__bank_account_balance = balance

    def get_account_balance(self) -> int:
        return self.__bank_account_balance

Raqeeb = TruePerson(name="Raqeeb", _age=20)
print(Raqeeb)

Raqeeb.set_bank_balance(100)
print(Raqeeb)

Raqeeb.get_account_balance()



# 3. Understanding Name Mangling and Its Purpose


# Example 2: Inheritance and Name Mangling

# One major reason for double underscore name mangling is to avoid attribute collisions in subclasses. Let’s see how that
# work

@dataclass
class Base:
    __private_var: str = "Base Private"

    def reveal(self):
        return self.__private_var
    

@dataclass
class Derived(Base):
    __private_var: str = "Derived Private"

    def reveal_derived(self):
        return self.__private_var
    

base = Base()
derived = Derived()

print(base.reveal())           # "Base Private"
print(derived.reveal())        # "Base Private" -> calls Base.reveal()
print(derived.reveal_derived())# "Derived Private"


# Explanation:
# 
# Base defines a double underscore attribute __private_var.
# Derived also defines a double underscore attribute named the same but is internally renamed to _Derived__private_var.
# When derived.reveal() is called, it uses Base.reveal(), which returns _Base__private_var → "Base Private".
# When derived.reveal_derived() is called, it returns _Derived__private_var → "Derived Private".
# 
# This shows how name mangling keeps attributes with the same “private” name in different classes from clashing.
# If we had used a single underscore _private_var, the subclass attribute would have overridden or conflicted with the base class attribute.
# 
# This is Example #2: illustrating why double underscores might be preferable when dealing with inheritance.





# 4. Using Properties to “Protect” Data in DataClasses
# 
# Example 3: A DataClass with a Private Field + Property
# 
# Although underscore conventions and name mangling provide a hint, we often want to control how the field is accessed or modified.
# Properties can handle that:



from dataclasses import dataclass, field

@dataclass
class Employee:
    name: str
    __salary: float = field(repr=False, default=0)  # Not shown in __repr__

    @property
    def salary(self) -> float:
        """Read-only property that returns the private salary."""
        return self.__salary

    @salary.setter
    def salary(self, new_salary: float):
        """Setter that validates the new salary."""
        if new_salary < 0:
            raise ValueError("Salary cannot be negative.")
        self.__salary = new_salary

emp = Employee(name="Alice")
print(emp)          # Employee(name='Alice')
print(emp.salary)   # 0
emp.salary = 55000
print(emp.salary)   # 55000
# emp.__salary   # Will raise AttributeError

# Key points:
# 
# - We store __salary as a “private” field.
# - We create a @property named salary to get (return self.__salary) and set (self.__salary = new_salary) the salary value.
# - Notice the use of repr=False in field(...): prevents the private field from appearing in the auto-generated repr.
# - This is Example #3, showing how you can combine data classes, name mangling, and properties for a more idiomatic “private” approach.
# 



# 5. Combining Protected Fields with Slots or Additional Methods
# 
# Example 4: A DataClass with _protected Attributes and Advanced Usage
# 
# Let’s create a data class that uses _protected_value to indicate a field that’s not meant for external usage, 
# but we’ll add methods to read/write it carefully.


from dataclasses import dataclass

@dataclass
class Settings:
    database_url: str
    _api_token: str    # Protected by convention

    def get_api_token(self) -> str:
        """A method to safely retrieve the protected token."""
        # Possibly perform logging or checks here
        return self._api_token

    def set_api_token(self, token: str):
        """A method to safely update the protected token."""
        if not token.startswith("tok_"):
            raise ValueError("API token must start with 'tok_'.")
        self._api_token = token

config = Settings(database_url="postgres://localhost", _api_token="tok_ABC123")
print(config.get_api_token())  # "tok_ABC123"

# Even though it's "protected", direct access is possible in Python:
config._api_token = "tok_Override"  # Not recommended, but won't crash
print(config.get_api_token())       # "tok_Override"

# Proper usage via setter
config.set_api_token("tok_NEW456")
print(config.get_api_token())  # "tok_NEW456"



# Notes:
# 
# - The single underscore _api_token clarifies “internal usage only.”
# - We provide dedicated methods: get_api_token() and set_api_token() with minimal logic.
# - In reality, a developer can still do config._api_token = "raw_token". 
#   This is Python’s “we’re all consenting adults” philosophy, but the underscore is a hint not to do that.
# - This is Example #4, showing a “protected” attribute with accessor methods.





# 6. Chaining It All Together in a More Complex DataClass
# 
# Example 5: Mixed Access Levels in One Class
# 
# Let’s build a real-world(ish) scenario with an e-commerce Order class containing:
# 
# - Public order_id
# - Protected _discount_code
# - Private __internal_tax_rate
# - Property-based logic to compute final price




from dataclasses import dataclass

@dataclass
class Order:
    order_id: int
    base_price: float
    _discount_code: str = ""         # Protected
    __internal_tax_rate: float = 0.1 # Private

    # The @property decorator turns the total_price method into a computed attribute.
    # This means that when you access order.total_price, Python automatically calls the method
    @property
    def total_price(self) -> float:
        """
        The final price factoring in discount (if any) and tax.
        """
        discounted = self.base_price
        if self._discount_code == "BLACKFRIDAY":
            discounted *= 0.5  # 50% off

        # Access the name-mangled attribute for final calculation
        return discounted + (discounted * self.__internal_tax_rate)

    def set_discount_code(self, code: str):
        """Method to safely set a discount code."""
        # We can implement checks, e.g. only certain codes are valid
        self._discount_code = code

# Usage
order = Order(order_id=101, base_price=100.0)
print(order.total_price)  # 110.0 (10% tax on 100)

order.set_discount_code("BLACKFRIDAY")
print(order.total_price)  # 55.0 (50% discount => 50, plus 10% tax => 5 => 55 total)

# Attempting direct private access:
# print(order.__internal_tax_rate)  # AttributeError
# But we can do:
print(order._Order__internal_tax_rate)  # 0.1, not recommended to do so externally!




# Explanation:
# 
# - Public: order_id and base_price.
# - Protected: _discount_code, indicating it is an internal detail about discounts that we set via set_discount_code().
# - Private: __internal_tax_rate, used only inside class methods.
# - Property: total_price uses the private tax rate to compute the final price after any discount.
# - This is Example #5, combining multiple levels of attribute visibility for a more “production-like” scenario.



# 
# Practical Takeaways:
# 
# - Python does not enforce private or protected:
#   - Double-underscore (“private”) attributes are just name-mangled but still accessible if someone tries hard enough.
#   - Single underscore (“protected”) is purely a convention to discourage external use.
# 
# - Use Properties to manage “get” and “set” logic:
#   - This is often the best practice to protect or validate data in a data class (or any class in Python).
# 
# - Name Mangling primarily helps avoid conflicts in inheritance or accidental overrides.
# 
# - When in Doubt, Keep It Simple:
#   - If you’re creating a library or large-scale system, use underscore conventions + docstrings to communicate intent.
#   - Resist overusing double underscores unless you have a specific naming-conflict scenario.
# 



# Final Summary:
# 
# - Private & Protected in Python are conventions rather than rigid rules.
# - Data classes add no special enforcement for private or protected attributes but integrate seamlessly with Python’s underscores and name-mangling.
# - By understanding these conventions, leveraging properties, and writing clear docstrings, you can create robust, maintainable, and “semi-private” data structures that convey your intentions to other developers.
# 
# Feel free to mix
