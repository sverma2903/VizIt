import pandas as pd
import traceback

class CodeExecutor:
    """
    A helper class that holds a reference to a DataFrame and executes Python code 
    that modifies it, returning status messages.
    """
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def execute_code_tool(self, code: str) -> str:
        """
        Executes the given Python code string in a local namespace where 'df' is the DataFrame.
        The code can modify 'df'. After execution, the updated 'df' is stored back in this object.
        """
        local_vars = {"df": self.df}
        try:
            print(f"Executing code: ")
            print(code)
            exec(code, {}, local_vars)
            if "df" in local_vars:
                self.df = local_vars["df"]
            return "Code executed successfully."
        except Exception as e:
            tb = traceback.format_exc()
            return f"Error executing code: {e}\nTraceback:\n{tb}"
