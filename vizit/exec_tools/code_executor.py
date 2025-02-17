import pandas as pd
import traceback
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
