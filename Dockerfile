FROM python:3.12-slim

# Configure Poetry
ENV POETRY_VERSION=1.7.1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

RUN apt-get update && apt-get install -y \
    gcc \
    libc-dev

# Install poetry separated from system interpreter
RUN python3 -m venv $POETRY_VENV \
	&& $POETRY_VENV/bin/pip install -U pip setuptools \
	&& $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Add `poetry` to PATH
ENV PATH="${POETRY_VENV}/bin:${PATH}"


RUN poetry config virtualenvs.in-project true

# Export in first position so that "python" calls are from .venv
ENV PATH="/app/.venv/bin:${PATH}"
ENV PYTHONPATH="/app/:${PYTHONPATH}"


COPY ./pyproject.toml .
COPY ./poetry.lock .
COPY ./README.md .

COPY ./app /app

RUN poetry install --no-interaction --no-dev

WORKDIR /app

EXPOSE 80
