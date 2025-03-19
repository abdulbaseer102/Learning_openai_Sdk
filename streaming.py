import os
from dotenv import load_dotenv
from typing import cast
import chainlit as cl
from openai.types.responses import ResponseTextDeltaEvent
from agents import (
    Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel,
)

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


history = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
    model=model
)


@cl.on_chat_start
async def start():
    cl.user_session.set("chat_history", [])
    cl.user_session.set("agent", history)
    await cl.Message(content="Welcome! How can I assist you today?").send()

@cl.on_message
async def main(message: cl.Message):
    msg = cl.Message(content="Thinking...")
    await msg.send()

    agent: Agent = cast(Agent, cl.user_session.get("agent"))
    history = cl.user_session.get("chat_history") or []
    history.append({"role": "user", "content": message.content})

   
    result = Runner.run_streamed(agent, history)
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            await msg.stream_token(event.data.delta)

    response_content = result.final_output
    msg.content = response_content
    await msg.update()

    history.append({"role": "assistant", "content": response_content})
    cl.user_session.set("chat_history", history)



