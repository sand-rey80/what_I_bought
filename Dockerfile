FROM python:3.10

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

#RUN apt-get install -y --no-cache supervisor
#COPY supervisord.conf /etc/supervisord.conf

RUN pip3 install poetry

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi --no-dev

Expose 80

#RUN apt-get -y install libsm6 libxext6 libxrender-dev
#CMD ["python3", "bot.py"]
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
CMD ["sh", "-c", "python3", "bot.py", "&", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]


#CMD ["supervisord", "-c", "/etc/supervisord.conf"]