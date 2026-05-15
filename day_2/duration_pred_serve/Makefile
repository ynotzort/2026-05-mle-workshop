MODEL_PATH=./models/2022-01.bin
export MODEL_PATH

MODEL_VERSION=model_v1_2022_01_dev
export MODEL_VERSION

.PHONY: serve
serve:
	uv run fastapi dev src/duration_pred_serve/serve.py
	
.PHONY: predict-test
predict-test:
	uv run python scripts/predict-test.py
	
.PHONY: docker_build
docker_build:
	docker build -t duration-prediction:latest .
	
.PHONY: docker_run
docker_run: docker_build
	docker run -it -p 8080:8080 duration-prediction:latest