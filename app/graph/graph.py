"""
app/graph/graph.py — defines the langgraph for the EIPS application

*  build_eips_graph() - Creates the graph structure with nodes for each agent.
*  SupervisorNode - A custom node that decides which agent to run next based on the state.
*  _make_agent_node() - A helper function to create nodes for each agent with the appropriate prompts and logic.
*  Defines the edges and routing logic for the graph.
*  websocket handler will run this graph for each user query, passing in the EIPSState and streaming back responses.
*  Provides a way to run the graph with a given state.

"""