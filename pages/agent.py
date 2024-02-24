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


class GoogleCalendarAddEventArgs(BaseModel):
    event_name: str = Field(examples=["会議"])
    start_at: str = Field(examples=["2023-11-04T19:00:00+09:00"])
    duration: Optional[str] = Field(description="HH:mm", examples=["01:00", "02:00"])


@tool("google-calendar-add-event", args_schema=GoogleCalendarAddEventArgs)
def google_calendar_add_event_tool(
    event_name: str, start_at: str, duration: Optional[str]
):
    """Google Calendar Add Event"""
    webhook_url = os.environ["MAKE_WEBHOOK_URL"]
    body = {
        "eventName": event_name,
        "startAt": start_at,
        "duration": duration,
    }
    result = requests.post(webhook_url, json=body)
    return f"Status: {result.status_code} - {result.text}"


@tool("clock")
def clock_tool():
    """Clock to get current datetime"""
    return datetime.now(ZoneInfo("Asia/Tokyo")).isoformat()


st.title("AIアシスタント")

input = st.text_input(label="何を依頼しますか？")

if input:
    with st.spinner("考え中..."):
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        agent = initialize_agent(
            tools=[google_calendar_add_event_tool, clock_tool],
            llm=llm,
            agent=AgentType.OPENAI_FUNCTIONS,
        )
        result = agent.run(input)
        st.write(result)
