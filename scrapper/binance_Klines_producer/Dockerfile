FROM python:3.9-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY binance_Klines_producer.py .

CMD ["python", "binance_Klines_producer.py"]
