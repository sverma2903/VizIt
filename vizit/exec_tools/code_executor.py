import pandas as pd
import traceback
import json

def summarize_dataframe(df: pd.DataFrame) -> str:
    """
    Returns a short textual summary of the DataFrame for use in LLM prompts.
    """
    lines = [
        f"Shape: {df.shape}",
        f"Columns: {list(df.columns)}",
        f"Info: {df.info()}",
        "Head:",
        df.head(5).to_string(index=False)
    ]
    return "\n".join(lines)

class CodeExecutor:
    """
    A helper class that holds a persistent local context (a dictionary) in which the
    DataFrame and any additional variables are stored. This context is used for executing
    Python code. Any changes to variables (including 'df') are retained across executions.
    """
    def __init__(self, df: pd.DataFrame):
        # Initialize the context with the provided DataFrame.
        self.context = {"df": df}
        
    def get_df(self) -> pd.DataFrame:
        """
        Returns the DataFrame stored in the context.
        """
        return self.context.get("df")
    
    def get_context_summary(self) -> str:
        """
        Returns a summary of the variables in the context.
        """
        df_summary = summarize_dataframe(self.get_df())
        other_vars = [name for name in self.context if name != "df"]
        summaries = {"DataFrame": df_summary}
        for name in other_vars:
            value = self.context[name]
            summaries[name] = f"Type: {type(value)}, Value: {value}"
            
        # Serialize the summaries to JSON with indentation for readability.
        dump = json.dumps(summaries, indent=4)
        print(dump)
        return dump

    def execute_code_tool(self, code: str) -> str:
        """
        Executes the provided Python code in the persistent local context.
        The code is expected to operate on variables available in the context,
        especially 'df', but it may also create other variables.
        Any new or modified variables are retained for subsequent executions.

        To avoid GUI-related issues when plotting (e.g., with matplotlib),
        we force the use of the non-interactive 'Agg' backend.
        """
        # Prepend a line to force the non-interactive backend for matplotlib.
        backend_setup = "import matplotlib; matplotlib.use('Agg')\n"
        full_code = backend_setup + code

        try:
            # Execute the modified code in the persistent context.
            print(f"Executing code:\n")
            print(full_code)
            exec(full_code, {}, self.context)
            print("Code executed successfully. Variables available:", list(self.context.keys()))
            return "Code executed successfully."
        except Exception as exc:
            tb = traceback.format_exc()
            return f"Error executing code: {exc}\nTraceback:\n{tb}"
