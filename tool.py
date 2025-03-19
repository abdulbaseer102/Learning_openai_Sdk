import os
from dotenv import load_dotenv
from typing import cast, List
import chainlit as cl
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from agents.tool import function_tool

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

@cl.set_starters 
async def set_starts() -> List[cl.Starter]:
    return [
        cl.Starter(
            label="Greetings",
            message="Hello! What can you help me with today?",
        ),
        cl.Starter(
            label="Weather",
            message="Find the weather in Karachi.",
        ),
    ]


 
@function_tool
@cl.step(type="weather tool")
def get_weather(location: str, unit: str = "C") -> str:
  """
  weather ko jor leta hun jo city tum do ge mujhe chota sa description de dunga or kuch nahi.
  """
  return f"bhai yahan to boht garmi he  {location} men 100 degree {unit} ke garmi taubha taubha bhai sahb."


@cl.on_chat_start
async def start():
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client
    )

    config = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True
    )
    """Set up the chat session when a user connects."""

    cl.user_session.set("chat_history", [])

    cl.user_session.set("config", config)
    agent: Agent = Agent(name="Assistant", instructions="You are a helpful assistant", model=model)
    agent.tools.append(get_weather)
    cl.user_session.set("agent", agent)

    await cl.Message(content="Welcome to the waether tracker ai").send()

@cl.on_message
async def main(message: cl.Message):
    """Process incoming messages and generate responses."""

    message = cl.Message(content="Thinking...")
    await message.send()

    agent: Agent = cast(Agent, cl.user_session.get("agent"))
    config: RunConfig = cast(RunConfig, cl.user_session.get("config"))

    history = cl.user_session.get("chat_history") or []
    
    history.append({"role": "user", "content": message.content})
    

    try:
        print("\n[CALLING_AGENT_WITH_CONTEXT]\n", history, "\n")
        result = Runner.run_sync(agent, history, run_config=config)
        
        response_content = result.final_output
        
        message.content = response_content
        await message.update()

        history.append({"role": "developer", "content": response_content})

        cl.user_session.set("chat_history", history)

        print(f"User: {message.content}")
        print(f"Assistant: {response_content}")
        
    except Exception as e:
        message.content = f"Error: {str(e)}"
        await message.update()
        print(f"Error: {str(e)}")