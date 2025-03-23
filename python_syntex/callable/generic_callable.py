# 4.2 Genrics Callable

# Generics let you parameterize a callable’s input or output types using TypeVar. For example:

from typing import Callable, TypeVar

T = TypeVar('T')  # Declare a type variable 'T'
U = TypeVar('U') # Declare a type variable 'U'

# A generic callable that transforms type T into type U

Transfromer = Callable[[T], U]

def apply_transformer(value: T, transforms: Callable[[T], U]) -> U:
    return transforms(value)

# Example 1: Transform an integer into a descriptive string.
def int_to_str(n:int) -> str:
    return f"the number is {n}"

result1 = apply_transformer(34, int_to_str)
print(result1)

#------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------
# Usage with Generics and DataClass
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

# TContext is a type variable used to parameterize our class.
TContext = TypeVar("TContext")

@dataclass
class PotionMixer(Generic[TContext]):
    # The mix function now only expects a context of type TContext and returns a string.
    mix: Callable[[TContext], str]

    def create_potion(self, context: TContext) -> str:
        return self.mix(context)
    

# Example mixing function that uses a context (here, a dictionary) to create a potion description.
def magical_mix(context: dict) -> str:
    secret = context.get("secret", "moonlight")
    return f"Potion of wonder with a hint of {secret}!"


# Create an instance of PotionMixer with our magical_mix function.
mixer = PotionMixer(mix=magical_mix)


# Create a potion using a context that defines the secret ingredient.
potion = mixer.create_potion({"secret": "dragon scale"})
print(potion)  # Outputs: 'Potion of Wonder with a hint of dragon scale!'


# ========================================================================================================================
# =========================================================================================================
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

# TStory is a type variable that will represent the type of "story details" we pass in.
TStory = TypeVar("TStory")

@dataclass
class StoryTeller(Generic[TStory]):
    """
    A generic class that tells stories based on a storytelling function and story details.
    The type of story details (TStory) can be anything (e.g., a string, dict, list).
    """
    # tell is a function that takes story details (TStory) and returns a string (the story).
    tell: Callable[[TStory], str]

    def narrate(self, details: TStory) -> str:
        """
        Uses the tell function to create a story from the given details.
        
        Args:
            details: The story details of type TStory.
        Returns:
            A string representing the finished story.
        """
        return self.tell(details)

# Example storytelling function that uses a string as story details.
def simple_tale(details: str) -> str:
    """
    Creates a simple story using a single word or phrase as the details.
    """
    return f"Once upon a time, there was a {details} that brought joy to everyone."

# Another storytelling function that uses a dictionary as story details.
def adventure_tale(details: dict) -> str:
    """
    Creates an adventure story using a dictionary to specify the hero and place.
    """
    hero = details.get("hero", "brave traveler")
    place = details.get("place", "mysterious forest")
    return f"Long ago, {hero} explored the {place} and found a hidden treasure!"

# Usage Example
if __name__ == "__main__":
    # Create a StoryTeller with the simple_tale function (uses string details).
    simple_storyteller = StoryTeller(tell=simple_tale)
    story1 = simple_storyteller.narrate("magical bird")
    print(story1)  # Output: "Once upon a time, there was a magical bird that brought joy to everyone."

    # Create a StoryTeller with the adventure_tale function (uses dict details).
    adventure_storyteller = StoryTeller(tell=adventure_tale)
    story2 = adventure_storyteller.narrate({"hero": "fearless knight", "place": "haunted castle"})
    print(story2)  # Output: "Long ago, fearless knight explored the haunted castle and found a hidden treasure!"

    # Another example with default values from adventure_tale.
    story3 = adventure_storyteller.narrate({})
    print(story3)  # Output: "Long ago, brave traveler explored the mysterious forest and found a hidden treasure!"