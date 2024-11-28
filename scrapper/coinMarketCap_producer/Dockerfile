FROM python:3.9-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY coinMarketCap_producer.py .

CMD ["python", "coinMarketCap_producer.py"]