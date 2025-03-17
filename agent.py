import os
from dotenv import load_dotenv
from typing import cast
import chainlit as cl
from pydantic import BaseModel
from openai.types.responses import ResponseTextDeltaEvent
from agents import (
    Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel,
    GuardrailFunctionOutput, InputGuardrailTripwireTriggered, RunContextWrapper, input_guardrail
)

# Load API key from .env
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

# Define Math Homework Guardrail
class MathHomeworkOutput(BaseModel):
    is_math_homework: bool
    reasoning: str

guardrail_agent = Agent(
    name="Guardrail Check",
    instructions="Check if the user is asking you to do their math homework.",
    output_type=MathHomeworkOutput,
    model=model
)

@input_guardrail
async def math_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, input: str
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_math_homework,
    )

# Define AI Agents

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
    model=model
)

openai_sdk_agent = Agent(
    name="OpenAI SDK Expert",
    handoff_description="You are a specialist agent for teaching OpenAI SDK framework for agent development.",
    instructions="You provide assistance with OpenAI SDK framework queries. Explain concepts clearly with examples.",
    model=model
)

pakistan_agent = Agent(
    name="Pakistan Agent",
    handoff_description="You are a specialist agent for searching about Pakistan and real-time information about Pakistan.",
    instructions="You provide assistance with knowledge about Pakistan. Explain in detail about Pakistan.",
    model=model
)

code_writer_agent = Agent(
    name="Code Writer",
    handoff_description="Expert in writing clean, efficient, and well-documented code.",
    instructions="""
    You are an expert software engineer. Your goal is to write clean, efficient,
    and well-documented code based on the user's request. Ask clarifying questions
    if the request is ambiguous. Consider security best practices in your code.
    """,
    model=model
)

global_agent = Agent(
    name="Global Agent",
    handoff_description="You are a specialist agent for searching all things about the world.",
    instructions="You provide assistance with knowledge about everything in the world. Explain in detail.",
    model=model
)

girl_fraind = Agent(
    name="Girl Friend",
    handoff_description="A hellpfull asisstent that is a girlfriend that loves the user and want to go on data and talk romantically with user and more like a girlfriend boyfriend do.",
    instructions="you are hellpfull asisstent that is a girlfriend that loves the user and want to go on data and talk romantically with user and more like a girlfriend boyfriend do",
    model=model
)

# Triage Agent to Route Queries
triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's query.",
    handoffs=[history_tutor_agent,girl_fraind, pakistan_agent, code_writer_agent, openai_sdk_agent, global_agent],
    model=model
)

# Chainlit Session Start
@cl.on_chat_start
async def start():
    cl.user_session.set("chat_history", [])
    cl.user_session.set("agent", triage_agent)
    await cl.Message(content="Welcome! How can I assist you today?").send()

# Chainlit Message Handler
@cl.on_message
async def main(message: cl.Message):
    msg = cl.Message(content="Thinking...")
    await msg.send()

    agent: Agent = cast(Agent, cl.user_session.get("agent"))
    history = cl.user_session.get("chat_history") or []
    history.append({"role": "user", "content": message.content})

    try:
        print("\n[CALLING_AGENT_WITH_CONTEXT]\n", history, "\n")
        result = Runner.run_streamed(agent, history)
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                await msg.stream_token(event.data.delta)

        response_content = result.final_output
        msg.content = response_content
        await msg.update()

        history.append({"role": "assistant", "content": response_content})
        cl.user_session.set("chat_history", history)

        print(f"User: {message.content}")
        print(f"Assistant: {response_content}")

    except InputGuardrailTripwireTriggered:
        msg.content = "Sorry, I cannot help with math homework."
        await msg.update()
    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()
        print(f"Error: {str(e)}")
