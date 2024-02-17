import json
import logging
import time
from typing import Type, Optional, Any

import dotenv
from langchain import hub
from langchain.agents import initialize_agent, AgentType, create_react_agent, AgentExecutor
from langchain_core.agents import AgentFinish
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_community.chat_models import ChatOpenAI, ChatGooglePalm
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
dotenv.load_dotenv()

from langchain_community.agent_toolkits import SlackToolkit
from langchain_community.tools.slack.base import SlackBaseTool
from langchain_community.tools.slack.get_message import SlackGetMessageSchema
from langchain_community.tools.slack import SlackGetMessage, SlackGetChannel
from langchain_core.pydantic_v1 import BaseModel, Field


import fastapi

from fastapi import FastAPI, Request, Response, Query

app = FastAPI(
    title="Get weather data",
    description="Retrieves current weather data for a location.",
    version="v1.0.0",
    servers=[{"url": "https://3aad-2404-7a87-5321-6600-8d66-afed-88ce-b12b.ngrok-free.app"}]
)


@app.get("/location", operation_id="GetCurrentWeather")
def get_current_weather(location: str = Query(..., description="The city and state to retrieve the weather for")):
    # Here you would add the logic to retrieve weather data for the given location
    return {"location": location, "temperature": "Example temperature data"}

@app.get("/search_shampoo", operation_id="SearchShampoo")
def search_shampoo():

    return {"shampoo": "Example shampoo data"}
