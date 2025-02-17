# vizit/pipeline/pipeline.py

import textwrap
import pandas as pd

from vizit.ingestion import load_data
from vizit.exec_tools.code_executor import CodeExecutor
from vizit.preprocessing.preprocessing_agent import create_preprocessing_agent
from vizit.viz_suggestion.viz_suggestion_agent import create_viz_suggestion_agent
from vizit.viz_code.viz_code_agent import create_viz_code_agent

from vizit.logging import logger

def summarize_dataframe(df: pd.DataFrame) -> str:
    """
    Returns a short textual summary of the DataFrame for use in LLM prompts.
    """
    lines = [
        f"Shape: {df.shape}",
        f"Columns: {list(df.columns)}",
        "Head:",
        df.head(5).to_string(index=False)
    ]
    return "\n".join(lines)

def run_pipeline(data_path: str):
    """
    Orchestrates the entire pipeline:
      1) Ingest data into a DataFrame
      2) Preprocessing: Agent code generation + execution
      3) Visualization suggestions (text only)
      4) Visualization code generation + execution
    """
    # Step 1: Ingestion
    df = load_data(data_path)
    executor = CodeExecutor(df)

    # Step 2: Preprocessing
    df_summary = summarize_dataframe(executor.df)
    logger.info(f"Initial DataFrame summary: {df_summary}")
    prep_agent = create_preprocessing_agent(executor)
    prompt_preprocess = textwrap.dedent(f"""
        We have the following DataFrame:
        {df_summary}

        Please write Python code to clean/transform 'df' as needed, 
        then call 'execute_code_tool' to run it.
    """).strip()
    logger.info("[Stage: Preprocessing]")
    for chunk in prep_agent.do(prompt_preprocess, background=False):
        print(chunk, end="", flush=True)
    logger.info("\n")

    # Step 3: Visualization Suggestion
    df_summary_after = summarize_dataframe(executor.df)
    sugg_agent = create_viz_suggestion_agent()
    prompt_suggestions = textwrap.dedent(f"""
        The DataFrame now looks like this:
        {df_summary_after}

        Suggest 2-4 meaningful visualizations (just text, no code).
    """).strip()
    logger.info("[Stage: Visualization Suggestion]")
    suggestions_text = ""
    for chunk in sugg_agent.chat(prompt_suggestions, background=False):
        print(chunk, end="", flush=True)
        suggestions_text += chunk
    logger.info("\n")

    # Step 4: Visualization Code
    code_agent = create_viz_code_agent(executor)
    prompt_viz_code = textwrap.dedent(f"""
        Based on the following DataFrame summary:
        {df_summary_after}

        And these suggested plots:
        {suggestions_text}

        Please produce Python code that creates the recommended visualizations 
        from 'df' and saves them as .png files. Then call 'execute_code_tool' to run it.
    """).strip()
    logger.info("[Stage: Visualization Code Generation]")
    for chunk in code_agent.do(prompt_viz_code, background=False):
        print(chunk, end="", flush=True)
    logger.info("\n")

    logger.info("[INFO] Pipeline complete. Final DataFrame shape:", executor.df.shape)
    # If you want to retrieve the final DF, you can do so via executor.df
