"""
02_nested_dataclasses.py - Working with nested dataclasses

This file demonstrates how to properly structure and work with nested dataclasses.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional
import json


# Good example: Well-structured nested dataclasses

@dataclass
class Address:
    street: str
    city: str
    state: str
    zip_code: str
    country: str = 'USA'



@dataclass
class Contact:
    email: str
    phone: Optional[str] = None



@dataclass
class Employe:
    name: str
    age: int
    department: str
    # Nested Data class
    address: Address
    # Another Nested Data class
    contact: Contact
    # List of nested dataclasses
    skills: List[str] = field(default_factory=list)

    def to_json(self) -> str:
        """Convert the employee data to json string."""

        return json.dumps(asdict(self), indent=2)

    def add_skill(self, skill: str) -> None:
        """Add a skill to the employee's skills list.""" 
        if skill not in self.skills:
            self.skills.append(skill)   


# Usage example - Good Pattern

def demo_good_usage():
    # Create address 
    address = Address(
        street="123 Tech Lane",
        city="San Francisco",
        state="CA",
        zip_code="94107"
    )
    # Create a contact object
    contact = Contact(
        email="john.doe@example.com",
        phone="555-123-4567"
    )

    # Create an employee object
    employee = Employe(
        name='John Doe',
        age=30,
        department='Engineering',
        address=Address(
            street='123 Main St',
            city='New York',
            state='NY',
            zip_code='10001'
        ),
        contact=Contact(
            email='john.doe@example.com',
            phone='(123) 456-7890'
        ),
        skills=['Python', 'Data Science', 'Machine Learning']
    )
     # Access nested attributes with proper dot notation
    print(f"Employee: {employee.name}")
    print(f"City: {employee.address.city}")
    print(f"Email: {employee.contact.email}")

    # Add a skill
    employee.add_skill("Machine Learning")
    print(f"Skills: {employee.skills}")

    # Convert to JSON
    print("\nEmployee JSON:")
    print(employee.to_json())

demo_good_usage()


