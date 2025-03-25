import asyncio
import os
from dotenv import load_dotenv
from typing import cast
import chainlit as cl
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from stripe_agent_toolkit.openai.toolkit import StripeAgentToolkit


load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")



stripe_agent_toolkit = StripeAgentToolkit(
    secret_key="sk_test_51R6T9HHrHRMU52A3GCAeTfEJPd1aS5JSdHnSBCRcEU0cGPfjzJzlwnCCN31VCokVe5478c16hqAuyYEVR5Vpc5rL00VeuK9U6K",
    configuration={
        "actions": {
            "payment_links": {
                "create": True,
            },
            "products": {
                "create": True,
            },
            "prices": {
                "create": True,
            },
        }
    },
)

agent = Agent(
    name="Stripe Agent",
    instructions="Integrate with Stripe effectively to support business needs.",
    tools=stripe_agent_toolkit.get_tools(),
    model="o3-mini",
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


