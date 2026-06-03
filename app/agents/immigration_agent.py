"""
Immigration Agent
  • Tracks visa / LCA / I-94 status
  • Sends expiration alerts
  • Predicts filing deadlines
"""
from __future__ import annotations
import json
from datetime import date, timedelta
from typing import Optional
 
from langchain_core.tools import tool
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage
from langchain.agents import create_agent
from langgraph.types import Command
 
from app.config import get_settings
from app.database import get_db_session
from app.graph.state import EIPSState
from sqlalchemy import text


# ------------------------------------
# Tools
# ------------------------------------

@tool
async def get_