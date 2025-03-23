from dataclasses import dataclass
from typing import ClassVar

@dataclass
class American:
    # Class variables (shared by all instances) for national attributes
    national_language: ClassVar[str] = "English"
    national_food: ClassVar[str] = "Hamburger"
    national_body_temprature: ClassVar[str] = 90

    # Instance variables (unique to each person)

    name: str
    age:str
    weight: float
    liked_food: str

    # Methods for simulating speech; uses the class variable for language

    def speaks(self):
        return f"{self.name} is speaking {self.national_language}."

    # Method for simulating eating; uses the class variable for food

    def eats(self):
        return f"{self.name} is eating {self.national_food}."

    # Method for simulating a national body temperature check
    def check_body_temp(self):
        return f"{self.name} have {self.national_body_temprature} degrees Fahrenheit."

    # Method for simulating a favorite food check

    def check_favorite_food(self):
        return f"{self.name} likes {self.liked_food}."

    # Method for simulating a greeting
    def greet(self):
        return f"Hello, my name is {self.name}!"

    # Static method to return the national language without needing an instance
    @staticmethod
    def country_language(): 
        return American.national_language

    
# caling the static method to show national language

print(American.country_language())


# Creating an instance of American class

john = American("John", "30", 70.5, "Hamburger")

# calling instance methods

print(john.speaks())
print(john.eats())
print(john.check_body_temp())



# Print the class variables (national characteristics) from the American class

print(American.national_language)
print(American.national_food)
print(American.national_body_temprature)



