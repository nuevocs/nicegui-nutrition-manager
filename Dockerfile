FROM python:3.11.3-slim
ARG VERSION

LABEL maintainer="Tat <tat@seriousexplosion.net>"

RUN python -m pip install nicegui

#WORKDIR /
WORKDIR /app
#WORKDIR /nicegui_nutrition_manager/app
#COPY nicegui_nutrition_manager /app/nicegui_nutrition_manager
# Furthermore dependencies
#COPY ./requirements.txt /requirements.txt
#RUN pip install -r /requirements.txt

ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    PYSETUP_PATH="/opt/pysetup"

ENV PATH="$POETRY_HOME/bin:$PATH"

RUN apt-get update && \
    apt-get install --no-install-recommends -y curl && \
    apt-get clean

RUN curl -sSL https://install.python-poetry.org/ | python -
RUN ls /app
# packages install
COPY pyproject.toml /pyproject.toml
RUN poetry install
# RUN #poetry install --only main
RUN poetry run playwright install

EXPOSE 8080

CMD python3 nicegui_nutrition_manager/main.py