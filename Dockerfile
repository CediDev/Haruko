FROM python:3.11-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
STOPSIGNAL SIGINT

COPY requirements.txt /requirements.txt
RUN python -m venv /venv && \
    /venv/bin/pip install --no-cache-dir -r requirements.txt

COPY . /app
WORKDIR /app

CMD [ "/venv/bin/python", "Selfiebot.py" ]
