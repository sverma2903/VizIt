# vizit/pipeline/pipeline.py

import textwrap
import pandas as pd

from vizit.ingestion import load_data
from vizit.exec_tools.code_executor import CodeExecutor
from vizit.stages.preprocessing.preprocessing_agent import create_preprocessing_agent
from vizit.stages.analysis.analysis import create_analyzer_agent
from vizit.stages.viz_suggestion.viz_suggestion_agent import create_viz_suggestion_agent
from vizit.stages.viz_code.viz_code_agent import create_viz_code_agent


from vizit.logging import logger

def run_pipeline(data_path: str, output_path: str):
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
    summary = executor.get_context_summary()
    logger.info(f"Initial context summary: {summary}")
    prep_agent = create_preprocessing_agent(executor)
    logger.info("[Stage: Preprocessing]")
    for chunk in prep_agent.do(summary, background=False):
        print(chunk, end="", flush=True)
    logger.info("\n")
    
    # Step 3: Analysis
    summary = executor.get_context_summary()
    logger.info(f"DataFrame summary after preprocessing: {summary}")
    analysis_agent = create_analyzer_agent(executor)
    prompt_analysis = summary
    logger.info("[Stage: Analysis]")
    for chunk in analysis_agent.do(prompt_analysis, background=False):
        print(chunk, end="", flush=True)
    logger.info("\n")

    # Step 4: Visualization Suggestion
    summary = executor.get_context_summary()
    sugg_agent = create_viz_suggestion_agent()
    prompt_suggestions = textwrap.dedent(f"""
        Current Context summary (contains all local variables that accessible to you):
        {summary}
    """).strip()
    logger.info("[Stage: Visualization Suggestion]")
    suggestions_text = ""
    for chunk in sugg_agent.chat(prompt_suggestions, background=False):
        print(chunk, end="", flush=True)
        suggestions_text += chunk
    logger.info("\n")

    # Step 5: Visualization Code
    code_agent = create_viz_code_agent(executor)
    prompt_viz_code = textwrap.dedent(f"""
        Current Context summary (contains all local variables that accessible to you):
        {summary}

        And these suggested plots:
        {suggestions_text}
        
        The visualizations should be saved in the output directory: {output_path}
        The output_path might not exist yet, so you may need to create it.
    """).strip()
    logger.info("[Stage: Visualization Code Generation]")
    for chunk in code_agent.do(prompt_viz_code, background=False):
        print(chunk, end="", flush=True)
    logger.info("\n")

    logger.info(f"[INFO] Pipeline complete. Final DataFrame shape: {executor.get_df().shape}")
    # If you want to retrieve the final DF, you can do so via executor.get_df()
