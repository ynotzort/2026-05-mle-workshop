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

### create a makefile
- create a folder `models` (`mkdir models`)
- create the `Makefile` (`touch Makefile`)
- now we can simply run `make train` instead of the uv command

### tests
- `uv add pytest`
- `mkdir tests`
- create a `__init__.py` inside the tests folder (`touch tests/__init__.py`)
- create a `test_train.py` file inside the tests folder (has to start with `test_`)
- run tests with `uv run pytest` or `make test`


## day 2

### create the project and add the dependencies
- create a top level folder `day_2` and change into it (`mkdir day_2` and `cd day_2`)
- create a new uv project: `uv init --lib --python 3.10 duration_pred_serve`
- change dir into `duration_pred_serve` (via `cd duration_pred_serve`)
- add dependencies from day1: `uv add scikit-learn==1.2.2 numpy==1.26.4`
- lets add testing and logging dependencies: `uv add pytest loguru`
- add a webserver dependency: `uv add "fastapi[standard]"`
- add requests dependency for testing the webserver `uv add --dev requests`
- copy model over from day_1: (`mkdir models` and `cp ../../day_1/models/2022-01.bin models/`)

### ping example for fastAPI
- create a `ping.py` file inside of `src/duration_pred_serve/` and open it.
- change the python virtual environment to use the correct day 2 environment: click on the bottom right where it said day_1 and click browse, then select `/workspaces/2026-05-mle-workshop/day_2/duration_pred_serve/.venv/bin/python` .
- run the webserver via `uv run fastapi dev src/duration_pred_serve/ping.py`

### implement serve functionality
- implement simple loading of the model file
- run it via `uv run python src/duration_pred_serve/serve.py`
- modify it it to contain a webserver and now run it via `uv run fastapi dev src/duration_pred_serve/serve.py` or via `make serve`
- for testing lets create `predict-test.py` inside of a folder `scripts` and run it via `make predict-test`

### environment variables
- you can create environment variables via `export HELLO=world`, this creates a variable named `HELLO` with a value `world`
- print out the value of a variable with `echo $HELLO`
- remove the variable via `unset HELLO`
- in python you can access those via `os.getenv()`
- alternatively via `BaseSettings` from the package `pydantic_settings`
- we define now `MODEL_PATH=./models/2022-01.bin`
- we add the export into the Makefile
- add MODEL_VERSION also

### use Docker
- create a Dockerfile
- build the image via `docker build -t duration-prediction:latest .`
- run it via `docker run duration-prediction:latest`
- or just use `make docker_run`

### lets deploy it to the world via fly.io
- install it via `curl -L https://fly.io/install.sh | sh` and then run as suggested `source ~/.bashrc`
- login via `fly auth login`
- deploy the app via `fly launch`
