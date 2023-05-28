FROM python:3.11.3-slim
ARG VERSION

LABEL maintainer="Tat <tat@seriousexplosion.net>"

RUN python -m pip install nicegui

WORKDIR /app

# Furthermore dependencies
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN playwright install

EXPOSE 8080

CMD python3 main.py