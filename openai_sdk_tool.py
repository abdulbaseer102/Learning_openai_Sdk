import asyncio
from typing import cast
import chainlit as cl
from agents import Agent, Runner, WebSearchTool, trace, set_default_openai_key



agent = Agent(
    name="Web searcher",
    instructions="You Know Every thing about pakistan.",
    tools=[WebSearchTool(user_location={"type": "approximate", "city": "New York"})],
)

@cl.on_chat_start
async def start():
    cl.user_session.set("agent", agent)
    await cl.Message(content="Welcome To Agent ").send()

@cl.on_message
async def main(message: cl.Message):
    msg = cl.Message(content="Thinking...")
    await msg.send()

    agent: Agent = cast(Agent, cl.user_session.get("agent"))

    result = await Runner.run(agent, message.content)

    response_content = result.final_output
    msg.content = response_content
    await msg.update()



