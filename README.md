# Financial Research Lab

Research and implementation of financial concepts.

## Setup Instructions

To run the notebooks and Python scripts in this repository, it is recommended to use a virtual environment.

### 1. Create a Virtual Environment

Open your terminal in the project root and run:

```bash
python3 -m venv venv
```

### 2. Activate the Virtual Environment

- **macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```
- **Windows:**
  ```bash
  venv\Scripts\activate
  ```

### 3. Install Dependencies

Once the virtual environment is activated, install the required packages:

```bash
pip install -r requirements.txt
```

### 4. Running Jupyter Notebooks

If you want to use the virtual environment in Jupyter:

```bash
python -m ipykernel install --user --name=venv --display-name "Python (Financial Lab)"
```

Then, you can start Jupyter:

```bash
jupyter notebook
```

## Notebook Output Hygiene

Before committing or pushing, clear notebook outputs so diffs stay readable:

```bash
python scripts/clean_notebook_outputs.py
```

To install the repository Git hooks:

```bash
sh scripts/install_git_hooks.sh
```

The pre-commit hook clears staged notebook outputs and re-stages the cleaned notebooks. The pre-push hook checks that no notebook outputs are saved.
