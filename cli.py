from dotenv import load_dotenv
load_dotenv()
import argparse
import sys
from vizit.pipeline.pipeline import run_pipeline

def main():
    parser = argparse.ArgumentParser(description="Vizit CLI: AI-driven data visualization pipeline")
    parser.add_argument("--data", type=str, required=True, help="Path to your dataset (CSV, Excel, or JSON).")
    args = parser.parse_args()

    try:
        run_pipeline(args.data)
    except Exception as e:
        print(f"[ERROR] Pipeline failed: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
