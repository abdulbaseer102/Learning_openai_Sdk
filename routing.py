import asyncio
import uuid
import os
import chainlit as cl
from dotenv import load_dotenv

from openai.types.responses import ResponseTextDeltaEvent

from agents import (
    Agent, 
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    RawResponsesStreamEvent, 
    Runner, 
    TResponseInputItem, 
    trace
)

# Load API Key
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

# Initialize AI Model
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# Define agents
french_agent = Agent(
    name="french_agent",
    instructions="You only speak French",
    model=model
)

spanish_agent = Agent(
    name="spanish_agent",
    instructions="You only speak Spanish",
    model=model
)

english_agent = Agent(
    name="english_agent",
    instructions="You only speak English",
    model=model
)

triage_agent = Agent(
    name="triage_agent",
    instructions="Handoff to the appropriate agent based on the language of the request.",
    handoffs=[french_agent, spanish_agent, english_agent],
    model=model
)


@cl.on_message
async def main(message: cl.Message):
    """Handles user messages and routes them to the correct language-specific agent."""
    conversation_id = str(uuid.uuid4().hex[:16])
    agent = triage_agent
    inputs: list[TResponseInputItem] = [{"content": message.content, "role": "user"}]

    # Chainlit message object for streaming
    response_msg = cl.Message(content="")

    with trace("Routing example", group_id=conversation_id):
        result = Runner.run_streamed(
            agent,
            input=inputs,
        )
        async for event in result.stream_events():
            if not isinstance(event, RawResponsesStreamEvent):
                continue
            data = event.data
            if isinstance(data, ResponseTextDeltaEvent):
                await response_msg.stream_token(data.delta)

    # Send the final response
    await response_msg.send()

    # Update session state
    cl.user_session.set("inputs", result.to_input_list())
    cl.user_session.set("agent", result.current_agent)
