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
