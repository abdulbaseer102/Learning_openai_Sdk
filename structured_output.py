import nest_asyncio
nest_asyncio.apply()
import asyncio
from pydantic import BaseModel
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
from dotenv import load_dotenv
import os

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable not found")


external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client = external_client,
)

config = RunConfig(
    model = model,
    model_provider = external_client,
    tracing_disabled = True
)

class Weather(BaseModel):
    location: str
    temperature: float
    summary: str

async def main():
    agent = Agent(
        name = "StructuredWeatherAgent",
        instructions = "Use the final_output tool with WeatherAnswer schema",
        output_type = Weather
    )

    out = await Runner.run(agent, "What is the temperature in pakistan", run_config = config)
    print(out.final_output.temperature)

if __name__ == "__main__":
    asyncio.run(main())