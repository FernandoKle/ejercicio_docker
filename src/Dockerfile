FROM python:3.11-slim

WORKDIR /app

ENV TZ="America/Argentina/Buenos_Aires"
ENV SERVIDOR="iotunam.duckdns.org"
ENV TOPICO_PUBLICA="iot2024/fernando/contador"

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app

CMD ["python", "/app/clienteMqtt.py"]