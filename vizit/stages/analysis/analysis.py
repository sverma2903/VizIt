import textwrap
from orion.agents.normal_agent import NormalAgent
from vizit.exec_tools.code_executor import CodeExecutor

def create_analyzer_agent(code_executor: CodeExecutor) -> NormalAgent:
    """
    An agent that, given a DataFrame summary, writes code to analyze the data
    and calls 'execute_code_tool' to execute it.
    """
    agent = NormalAgent(
        name="AnalyzerAgent",
        role="assistant",
        description=textwrap.dedent("""
            You are the data analysis agent.
            Given a summary of the DataFrame and some more information about it, You are supposed to produce python code to analyze the data to find insights and statistics
            which can aid in data visualization, for finding what kinds of interesting visualizations to generate.
            Then call 'execute_code_tool' to run the code.
            The code should operate on a variable called 'df'.
            You can even do data engineering and feature engineering.
            Any new variables that you create should be stored in a 'insights' dictionary.
        """).strip(),
        model_name="o1",
        tools=[code_executor.execute_code_tool],
    )
    return agent