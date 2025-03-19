
import os
import chainlit as cl
from pydantic import BaseModel
from dotenv import load_dotenv
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
    AsyncOpenAI,
    OpenAIChatCompletionsModel
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


# Define guardrail output model
class MathHomeworkOutput(BaseModel):
    reasoning: str
    is_math_homework: bool


# Guardrail agent
guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking you to do their math homework.",
    output_type=MathHomeworkOutput,
    model=model
)


@input_guardrail
async def math_guardrail(
    context: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    """This is an input guardrail function, which calls an agent to check if the input is a math homework question."""
    result = await Runner.run(guardrail_agent, input, context=context.context)
    final_output = result.final_output_as(MathHomeworkOutput)

    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=final_output.is_math_homework,
    )

@cl.on_chat_start
async def setup_chat_bot():
    await cl.Message("Welcome to the Guardrail bot").send()


# Main Chainlit function
@cl.on_message
async def main(message: cl.Message):
    agent = Agent(
        name="Customer support agent",
        instructions="You are a customer support agent. You help customers with their questions.",
        input_guardrails=[math_guardrail],
        model=model
    )

    input_data: list[TResponseInputItem] = [
        {
            "role": "user",
            "content": message.content,
        }
    ]

    try:
        result = await Runner.run(agent, input_data)
        await cl.Message(content=result.final_output).send()
    except InputGuardrailTripwireTriggered:
        refusal_message = "Sorry, I can't help you with your math homework."
        await cl.Message(content=refusal_message).send()
