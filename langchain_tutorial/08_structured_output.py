# First we initialize the model we want to use.
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o", temperature=0)

# For this tutorial we will use custom tool that returns pre-defined values for weather in two cities (NYC & SF)

from typing import Literal
from langchain_core.tools import tool


@tool
def get_weather(city: Literal["nyc", "sf"]):
    """Use this to get weather information."""
    if city == "nyc":
        return "It might be cloudy in nyc"
    elif city == "sf":
        return "It's always sunny in sf"
    else:
        raise AssertionError("Unknown city")


tools = [get_weather]

# Define the structured output schema

from pydantic import BaseModel, Field


class WeatherResponse(BaseModel):
    """Respond to the user in this format."""

    conditions: str = Field(description="Weather conditions")


# Define the graph

from langgraph.prebuilt import create_react_agent

graph = create_react_agent(
    model,
    tools=tools,
    # specify the schema for the structured output using `response_format` parameter
    response_format=WeatherResponse,
)

inputs = {"messages": [("user", "What's the weather in NYC?")]}
response = graph.invoke(inputs)

print(response["structured_response"])
