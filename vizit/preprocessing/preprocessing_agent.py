import textwrap
from orion.agents.normal_agent import NormalAgent
from vizit.exec_tools.code_executor import CodeExecutor

def create_preprocessing_agent(code_executor: CodeExecutor) -> NormalAgent:
    """
    Creates a dedicated agent for data preprocessing.
    The agent can generate Python code to clean the data and call 'execute_code_tool' to run it.
    """
    agent = NormalAgent(
        name="PreprocessingAgent",
        role="assistant",
        description=textwrap.dedent("""
            You are the data preprocessing agent. 
            You receive a summary of a DataFrame, and the first 5 rows of the dataframe itself in csv, and you are supposed to produce Python code to clean or transform it
            (e.g., handle missing values, outliers).
            You can cal the execute_code_tool method to run the code.
        """).strip(),
        model_name="o1",
        tools=[code_executor.execute_code_tool],
    )
    return agent
