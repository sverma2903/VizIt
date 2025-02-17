import textwrap
from orion.agents.normal_agent import NormalAgent
from vizit.exec_tools.code_executor import CodeExecutor

def create_viz_code_agent(code_executor: CodeExecutor) -> NormalAgent:
    """
    An agent that, given a DataFrame summary and plot suggestions, writes code to generate the plots
    and calls 'execute_code_tool' to execute it.
    """
    agent = NormalAgent(
        name="VizCodeAgent",
        role="assistant",
        description=textwrap.dedent("""
            You are the visualization code generation agent.
            Given a summary of the DataFrame and a set of suggested plots, 
            produce Python code (using e.g. matplotlib or Plotly) to create those plots.
            Then call 'execute_code_tool' to run the code. 
            The code should operate on a variable called 'df' and save the plots as .png files.
        """).strip(),
        model_name="o1",
        tools=[code_executor.execute_code_tool],
    )
    return agent
