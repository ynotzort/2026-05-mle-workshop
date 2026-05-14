# 2026-05-mle-workshop

## day 1

this project is based on https://github.com/ynotzort/ml-engineering-contsructor-workshop

## how to install uv

just run `curl -LsSf https://astral.sh/uv/install.sh | sh`

## day 1 steps

### get the notebook

- create a new folder `day_1` (`mkdir day_1`)
- change into the directory `day_1` (`cd day_1`)
- get the original notebook:
```bash
mkdir notebooks
cd notebooks
wget "https://raw.githubusercontent.com/ynotzort/2025-07-mle-workshop/refs/heads/main/day_1/notebooks/duration-prediction-starter.ipynb"
cd ..
```

### create a uv project
- initialize a uv project with `uv init --python 3.10`
- run `uv sync`

### install dependencies
- `uv add scikit-learn==1.2.2 pandas pyarrow`
- `uv add --dev jupyter seaborn`
- now lets fix the error with numpy: `uv add numpy==1.26.4`

### launch jupyter notebook
- `uv run jupyter notebook`

### make vscode recognize the python env correctly and use jupyter from within vscode
- open a .py file (main.py)
- on the bottom right click on the python version -> browse -> find the path to python (here it was /workspaces/2026-05-mle-workshop/day_1/.venv/bin/python)
- go to the jupyter notebook file and click select kernel -> python environments -> day_1

### convert the notebook into a script
- `uv run jupyter nbconvert --to=script notebooks/duration-prediction-starter.ipynb`
- create a folder named `duration_prediction` (`mkdir duration_prediction`)
- move the freshly created file `notebooks/duration-prediction-starter.py` into `duration_prediction` and rename it to `train.py`

# lets make the train.py script nice
- remove all # lines from the script
- move all imports to the top
- remove matplotlib abd seaborn
- ctrl+shift+p format document (ruff or something else) (optional)
- try to run it `uv run python duration_prediction/train.py`
- create a train function and remove top-level statements and add `if __name__ == "__main__":`
- add the pipeline code
- parametrize the train function
- use argparse to parse arguments
    - alternatives are https://github.com/fastapi/typer and click and fire
    - now run with `uv run python duration_prediction/train.py --train-date 2022-01 --val-date 2022-02 --model-save-path model.bin`
- add docstrings and typing
- add simple error handling
- add logging: `uv add loguru`
- split our the argparse into a `main.py` and make it a module by adding a `__init__.py` file. now we have to call `uv run python -m duration_prediction.main --train-date 2022-01 --val-date 2022-02 --model-save-path model.bin` in order to run it. notice the -m for module mode in python.
