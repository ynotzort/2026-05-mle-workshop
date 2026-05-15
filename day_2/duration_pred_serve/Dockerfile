FROM python:3.10-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:0.11.14 /uv /uvx /bin/

# copy over our project files
ADD pyproject.toml uv.lock README.md src/ /app/

WORKDIR /app/

RUN uv sync --frozen

# copy over the model
ADD models/2022-01.bin 2022-01.bin

# set the env variables
ENV MODEL_PATH=2022-01.bin
ENV MODEL_VERSION=v1_2022_01
ENV LOGURU_LEVEL=INFO

# expose the port
EXPOSE 8080

ENTRYPOINT [ "uv", "run", "fastapi", "run", "/app/duration_pred_serve/serve.py", "--port", "8080" ]
