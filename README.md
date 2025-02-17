# Vizit

Vizit is an AI-driven data visualization pipeline that leverages [Orion](https://github.com/AshishKumar4/Orion) agents and OpenAI’s language models to automatically ingest, preprocess, analyze, and visualize your data. With Vizit, you can transform raw datasets into beautiful, insightful visualizations with minimal manual intervention.

---

## Table of Contents

- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Installation](#installation)
- [Usage](#usage)
  - [Command Line Interface (CLI)](#command-line-interface-cli)
  - [Example Workflow](#example-workflow)
- [Configuration](#configuration)
- [Extending Vizit](#extending-vizit)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Data Ingestion:**  
  Load datasets in CSV, Excel, or JSON formats into a Pandas DataFrame.
- **Automated Preprocessing:**  
  An Orion agent generates and executes Python code to clean or transform your data.
- **Data Analysis:**  
  A dedicated stage where an Orion agent generates code to compute summary statistics or other data analysis metrics. The results (e.g., new variables, computed statistics) are stored in a persistent execution context.
- **Visualization Suggestion:**  
  An Orion agent analyzes the current state of the data and provides textual recommendations for meaningful plots.
- **Visualization Code Generation:**  
  Another Orion agent generates Python code to create the suggested visualizations (using libraries such as Plotly or matplotlib) and executes the code to save the plots as image files.
- **Persistent Execution Context:**  
  A custom `CodeExecutor` maintains a persistent local namespace that retains all variables created or modified across different stages.
- **Retry Mechanism:**  
  If generated code fails to execute, the agent is notified of the error and asked to regenerate its code.
- **Modular & Object-Oriented:**  
  The pipeline is organized into clear, independent stages (ingestion, preprocessing, data analysis, visualization suggestion, and visualization code generation) for ease of extension and maintenance.

---

## Architecture Overview

Vizit’s pipeline consists of the following stages:

1. **Ingestion:**  
   Reads a dataset from a specified file and loads it into a Pandas DataFrame.

2. **Preprocessing:**  
   An Orion agent generates Python code to clean or transform the DataFrame. This code is executed using the persistent `CodeExecutor`.

3. **Data Analysis:**  
   An additional Orion agent generates and executes code to perform further analysis on the data (for example, computing summary statistics or new derived metrics).  
   All results are retained in the persistent context.

4. **Visualization Suggestion:**  
   Based on a summary of the analyzed data, another Orion agent returns textual suggestions for visualizations (e.g., "a histogram of ages" or "a scatter plot of score vs. age").

5. **Visualization Code Generation:**  
   Finally, an Orion agent generates Python code to create the recommended plots and execute that code to save the visualizations as image files.

*Note: Vizit does not use a generic AgentRunner; each stage creates its own agent and directly integrates code execution with retry logic via the persistent `CodeExecutor`.*

---

## Installation

Vizit requires Python 3.8 or higher. To install Vizit, clone the repository and install the package in editable mode:

```bash
git clone https://github.com/yourusername/vizit.git
cd vizit
pip install -e .
```

Dependencies (including Orion, pandas, openai, plotly, etc.) are specified in the `pyproject.toml` file.

---

## Usage

### Command Line Interface (CLI)

Vizit includes a simple CLI tool. To run the complete pipeline on your dataset, use:

```bash
python cli.py --data /path/to/your/dataset.csv --output /path/to/output_directory
```

- **--data:** Path to your dataset (supported formats: CSV, Excel, JSON).
- **--output:** Directory where generated visualization files will be saved (Vizit will create this directory if it does not exist).

### Example Workflow

1. **Data Ingestion:**  
   Vizit reads your dataset from the provided file and loads it into a DataFrame.

2. **Preprocessing Stage:**  
   The preprocessing agent receives a summary of the data and generates Python code to clean or transform it.  
   The code is executed in a persistent context (via `CodeExecutor`), preserving any new variables or analysis results.

3. **Data Analysis Stage:**  
   An analysis agent further processes the data to compute summary statistics or create derived metrics.  
   These results are stored in the persistent context and can be used by later stages.

4. **Visualization Suggestion Stage:**  
   Based on the updated data summary, the visualization suggestion agent provides textual recommendations for plots.

5. **Visualization Code Generation Stage:**  
   Finally, the visualization code agent generates Python code to create and save the recommended plots as PNG files in the specified output directory.

After running the pipeline, check your output directory to view the generated visualizations.

---

## Configuration

Before running Vizit, ensure that you have set the following environment variables:

- **OPENAI_API_KEY:** Your OpenAI API key for accessing language models.
- **ORION_MODEL_NAME:** (Optional) Specifies the Orion model to use (default is `"gpt-4o"`).

You can set these in your terminal:

```bash
export OPENAI_API_KEY="sk-..."
export ORION_MODEL_NAME="gpt-4o"
```

---

## Extending Vizit

Vizit is designed to be modular and extensible. Some ideas for extension include:

- **Web Interface:**  
  Build a Flask or FastAPI application to serve visualizations interactively.
  
- **Additional Analysis:**  
  Add more specialized data analysis agents to compute advanced statistics or machine learning metrics.
  
- **Custom Agents:**  
  Modify or extend the Orion agents to handle domain-specific preprocessing or visualization tasks.
  
- **Improved Logging:**  
  Integrate more granular logging or error monitoring for production environments.

---

## Contributing

Contributions are welcome! If you have ideas for new features, bug fixes, or improvements, please submit a pull request or open an issue on the GitHub repository.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/my-feature`).
3. Commit your changes.
4. Push your branch and open a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- This project leverages the Orion library by [AshishKumar4](https://github.com/AshishKumar4/Orion) for agent-based interactions.
- Special thanks to the contributors of OpenAI’s language models and the Python data science ecosystem.
```

Feel free to adjust any sections as needed to best fit your project’s specifics.
