import textwrap
from orion.agents.normal_agent import NormalAgent

def create_viz_suggestion_agent() -> NormalAgent:
    """
    An agent that, given a summary of the DataFrame, suggests possible visualizations (in text only).
    """
    agent = NormalAgent(
        name="VizSuggestionAgent",
        role="assistant",
        description=textwrap.dedent("""
            You are a visualization suggestion agent. 
            Given a summary of the DataFrame and some more information about it, along with some statistics and insights from it, propose handful of meaningful charts or plots
            that would provide interesting insights into the data. Provide only textual suggestions, no code.
        """).strip(),
        model_name="o1",
        tools=[],
    )
    return agent
