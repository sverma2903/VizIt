import os
import pandas as pd

def load_data(path: str) -> pd.DataFrame:
    """
    Loads a dataset (CSV, Excel, or JSON) into a Pandas DataFrame and stores it in DATA_STORE.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found at {path}")

    ext = os.path.splitext(path)[1].lower()
    try:
        if ext == ".csv":
            df = pd.read_csv(path)
        elif ext in [".xlsx", ".xls"]:
            df = pd.read_excel(path)
        elif ext == ".json":
            df = pd.read_json(path)
        else:
            raise ValueError(f"Unsupported file extension: {ext}")

        print(f"[INFO] Loaded data from {path} with shape {df.shape}")
        
        return df
    except Exception as e:
        raise RuntimeError(f"Error loading {path}: {e}")
