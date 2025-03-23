# Advanced: Using Generic[T] in LLM-based Agents

# Here’s a real-world example where Generic[T] is used in an AI agent class.

# from typing import Generic, TypeVar

# TContext = TypeVar("TContext")

# class Agent(Generic[TContext]):
#     """A generic AI agent that works with different contexts."""

#    def __init__(self, name: str, context: TContext):
#         self.name = name
#        self.context = context

#    def execute(self) -> None:
#        print(f"Executing with context: {self.context}")

# Creating agents with different contexts
# text_agent = Agent[str]("TextProcessor", "Analyze sentiment")
# data_agent = Agent[dict]("DataAnalyzer", {"data": [1, 2, 3]})

# text_agent.execute()  # Executing with context: Analyze sentiment
# data_agent.execute()  # Executing with context: {'data': [1, 2, 3]}
# ✅ Why is this useful?

# The same Agent class works with any context type (text, dict, etc.).
# It avoids code duplication.



from typing import Generic, TypeVar

TContext = TypeVar("TContext")

class Agent(Generic[TContext]):
    """A generic AI agent that works with different contexts."""

    def __init__(self, name: str, context: TContext):
        self.name = name
        self.context = context

    def execute(self) -> None:
        print(f"Executing with context: {self.context}")

# Creating agents with different contexts
text_agent = Agent[str]("TextProcessor", "Analyze sentiment")
data_agent = Agent[dict]("DataAnalyzer", {"data": [1, 2, 3]})

text_agent.execute()  # Executing with context: Analyze sentiment
data_agent.execute()  # Executing with context: {'data': [1, 2, 3]}
     