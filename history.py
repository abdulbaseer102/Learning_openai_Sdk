import os
from dotenv import load_dotenv
from typing import cast
import chainlit as cl
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



# Initialize Agent

openai_sdk_agent = Agent(
    name="OpenAI SDK Expert",
    handoff_description="You are a specialist agent for teaching OpenAI SDK framework for agent development.",
    instructions="You provide assistance with OpenAI SDK framework queries. Explain concepts clearly with examples.",
    model=model
)

# Initialize Runner

@cl.on_chat_start
async def start():
    cl.user_session.set("chat_history", [])
    cl.user_session.set("agent", openai_sdk_agent)
    await cl.Message(content="Welcome To History Agent I Reminde EverySingle Thing You Tell Me").send()

@cl.on_message
async def main(message: cl.Message):
    msg = cl.Message(content="Thinking...")
    await msg.send()

    agent: Agent = cast(Agent, cl.user_session.get("agent"))
    history = cl.user_session.get("chat_history") or []
    history.append({"role": "user", "content": message.content})
    
    result = await Runner.run(agent, history)

    response_content = result.final_output
    msg.content = response_content
    await msg.update()

    history.append({"role": "assistant", "content": response_content})
    cl.user_session.set("chat_history", history)