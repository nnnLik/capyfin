ARG PYTHON_IMAGE=python:3.12-slim

FROM $PYTHON_IMAGE AS base

ENV PYTHONOPTIMIZE=2 \
	PYTHONUNBUFFERED=1 \
	PYSETUP_PATH="/opt/pysetup" \
	VENV_PATH="/opt/pysetup/.venv" \
	APP_PATH="/opt/app/src" \
	PYTHONPATH="/opt/app/src"

RUN apt-get update && \
	pip install uv==0.5.20 && \
	rm -rf /var/lib/apt/lists/*

WORKDIR $PYSETUP_PATH

FROM base AS builder

COPY pyproject.toml uv.lock $PYSETUP_PATH/
RUN uv sync --group=prod
ENV PATH="$VENV_PATH/bin:$PATH"

FROM builder AS dev

RUN apt-get update && apt-get install -y --no-install-recommends curl vim htop && \
	apt-get clean && rm -rf /var/lib/apt/lists/*

RUN uv sync --group=dev

COPY --from=builder $VENV_PATH $VENV_PATH
COPY ./src/ ${APP_PATH}

WORKDIR ${APP_PATH}
