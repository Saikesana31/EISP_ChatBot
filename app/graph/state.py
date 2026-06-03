"""

-EIPSState(TypedDict) that flows through each node.
- It contains the message history, routing decison(next), user identity/role.
- Also agent_outputs: A dict that contains the outputs of each agent, which can be used by supervisor 
- when 2 agents run parallelly and supervisor needs to make a decision based on the outputs of both agents.    

"""

from typing import List, Dict, Any, Literal, Optional
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from typing_extensions import Annotated,TypedDict



Agentnames = Literal[
    "Immigration Agent",
    "payroll Agent",
    "timesheets_agent",
    "document_agent",
    "Analytics_agent",
    "Assignment_agent",
]

class EIPSState(TypedDict):
    
    # Conversation history
    messages : Annotated[list[BaseMessage],add_messages] 
    """
    The conversation history between the user and the agents. 
    This should include all messages exchanged, including those from the user and all agents. 
    Each message should have a role (e.g., 'user') and content.
    add_message reducer on messages filed appends(not replaced)
    
    """
    # Routing Decision(next agent to run)- The supervisor writes 'next' to control which agent should run next.
    next: Agentnames
    
    # Session Context
    """
    Here we can store User Role/identity
    E.g : admin/Hr/Manager/Employee etc.
    """
    Session_id : str
    user_id : str
    user_role : str
    user_email : str
    
    # Agent outputs - A dict that contains the outputs of each agent, which can be used by supervisor
    
    agent_outputs : dict[str,str]
    
    
