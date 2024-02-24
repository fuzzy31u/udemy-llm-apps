import os
from datetime import datetime
from typing import Optional

import langchain
import requests
import streamlit as st
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools import tool
from pydantic import BaseModel, Field
from zoneinfo import ZoneInfo

langchain.verbose = True


class XPostEventArgs(BaseModel):
    post_content: str = Field(examples=["サンプルテキスト"])

@tool("google-calendar-search-event")
def google_calendar_search_event_tool():
    """Google Calendar Search Event"""
    webhook_url = os.environ["MAKE_WEBHOOK_CALENDAR_SEARCH_URL"]
    result = requests.get(webhook_url)
    
    try:
        json_data = result.json()
        print(f"Response JSON: {json_data}")
    except ValueError:
        print("Response is not JSON format.")

    return f"[Search Calendar]Status: {result.status_code} - {result.text}"

@tool("clock")
def clock_tool():
    """Clock to get current datetime"""
    return datetime.now(ZoneInfo("Asia/Tokyo")).isoformat()

@tool("x-post-event", args_schema=XPostEventArgs)
def x_post_event_tool(
    post_content: str
):
    """X Post Event"""
    webhook_url = os.environ["MAKE_WEBHOOK_X_URL"]
    body = {
        "postContent": post_content,
    }
    result = requests.post(webhook_url, json=body)
    return f"[Post X]Status: {result.status_code} - {result.text}"


st.title("X投稿アシスタント w/ Google Calendar")

input = st.text_input(label="何の投稿を依頼しますか？")

if input:
    with st.spinner("投稿中..."):
        llm = ChatOpenAI(model="ft:gpt-3.5-turbo-0613:personal::8uXqAnqZ", temperature=0)
        agent = initialize_agent(
            tools=[clock_tool, google_calendar_search_event_tool, x_post_event_tool],            
            llm=llm,
            agent=AgentType.OPENAI_FUNCTIONS,
        )
        result = agent.run(input)
        st.write(result)
