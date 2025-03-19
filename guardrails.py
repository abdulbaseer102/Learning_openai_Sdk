from pydantic import BaseModel
import os
from dotenv import load_dotenv
from typing import cast
import chainlit as cl
from openai.types.responses import ResponseTextDeltaEvent
from agents import (
    Agent,
    AsyncOpenAI, 
    OpenAIChatCompletionsModel, 
    GuardrailFunctionOutput,
    OutputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    output_guardrail,
)

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

class MessageOutput(BaseModel): 
    response: str

class MathOutput(BaseModel): 
    is_math: bool
    reasoning: str

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the output includes any math.",
    output_type=MathOutput,
    model=model
)

@output_guardrail
async def math_guardrail(  
    ctx: RunContextWrapper, agent: Agent, output: MessageOutput
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, output.response, context=ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output.model_dump(),  # JSON Serialization
        tripwire_triggered=result.final_output.is_math,
    )

agent = Agent( 
    name="Customer support agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    output_guardrails=[math_guardrail],
    output_type=MessageOutput,
    model=model
)

@cl.on_chat_start
async def start():
    cl.user_session.set("agent", agent)
    await cl.Message(content="Welcome! How can I assist you today NOTE:DONT TELL ME ABOUT MATH?").send()

@cl.on_message
async def main(message: cl.Message):
    msg = cl.Message(content="Thinking...")  
    await msg.send()

    agent: Agent = cast(Agent, cl.user_session.get("agent"))

    try:
        print("\n[CALLING_AGENT_WITH_CONTEXT]\n", message.content, "\n")
        result = Runner.run_streamed(agent, message.content)
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                await msg.stream_token(event.data.delta)

        response_content = result.final_output.model_dump()
        msg.content = response_content 
        await msg.update()

        print(f"User: {message.content}")
        print(f"Assistant: {response_content}")

    except OutputGuardrailTripwireTriggered:
        msg.content = "⚠️ i can procces about this content"
        await msg.update()
        print("🚨 Math output guardrail tripped")