#FROM python:3.10-slim-buster

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.8.4

COPY . .

#RUN apt-get install curl --no-install-recommends -y
#RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 -

RUN pip3 install poetry

RUN poetry config virtualenvs.create false && \
 poetry install --no-interaction --no-ansi --only main --no-root

EXPOSE 8000

#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" "--proxy-headers"]
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]


