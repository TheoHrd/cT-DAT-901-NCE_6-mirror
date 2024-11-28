import configparser
import json
import sys

import requests
from kafka import KafkaProducer
import time

class BinanceKlinesProducer:
    def __init__(self, symbols=None, config_file='config.ini', interval='1m'):
        if symbols is None:
            symbols = ['btcusdt', 'ethusdt', 'bnbusdt', 'xrpusdt', 'solusdt', 'trxusdt']

        config = configparser.ConfigParser()
        config.read(config_file)
        self.symbols = [str(symbol).lower() for symbol in symbols]
        self.interval = interval
        self.topic = config['kafka']['TopicIn_BinanceKlines']
        self.kafka_servers = config['kafka']['kafkaServers']
        self.producer = KafkaProducer(
            bootstrap_servers=self.kafka_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda v: v if isinstance(v, bytes) else v.encode('utf-8')
        )

    @staticmethod
    def get_klines(symbol, interval, limit=10):
        url = 'https://api.binance.com/api/v3/klines'
        params = {
            'symbol': symbol.upper(),
            'interval': interval,
            'limit': limit
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"Erreur API Binance pour {symbol}: {response.status_code}, {response.text}")
            return None
        return response.json()

    def process_klines(self, symbol):
        klines = self.get_klines(symbol, self.interval)
        if klines is None:
            return

        for kline in klines:
            data = {
                "symbol": symbol,
                "open_time": kline[0],
                "open": kline[1],
                "high": kline[2],
                "low": kline[3],
                "close": kline[4],
                "volume": kline[5],
                "close_time": kline[6]
            }
            self.producer.send(
                self.topic,
                key=symbol.encode('utf-8'),
                value=data
            )
            print(f"Klines Datas : {data}")

    def start(self):
        try:
            while True:
                for symbol in self.symbols:
                    self.process_klines(symbol)
                time.sleep(60)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        print('Interruption reçue, fermeture du producteur Kafka.')
        if self.producer:
            self.producer.close()
        sys.exit(0)


if __name__ == "__main__":
    def get_usdt_pairs():
        url = 'https://api.binance.com/api/v3/exchangeInfo'
        response = requests.get(url)
        data = response.json()
        usdt_pairs = []
        for symbol in data['symbols']:
            if symbol['quoteAsset'] == 'USDT' and symbol['status'] == 'TRADING':
                usdt_pairs.append(symbol['symbol'].lower())
        return usdt_pairs

    symbols = get_usdt_pairs()

    producer = BinanceKlinesProducer(symbols=None, interval='5m')

    try:
        producer.start()
    except KeyboardInterrupt:
        producer.stop()