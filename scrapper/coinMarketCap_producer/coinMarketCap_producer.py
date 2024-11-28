import configparser
import json
import sys

import requests
from kafka import KafkaProducer
import time


class CoinMarketCapProducer:
    def __init__(self, symbols=None, config_file='config.ini'):
        if symbols is None:
            symbols = ['btcusdt', 'ethusdt']

        config = configparser.ConfigParser()
        config.read(config_file)
        self.symbols = [str(symbol).lower() for symbol in symbols]
        self.topic = config['kafka']['TopicIn_CoinMarketCap_Coin']
        self.kafka_servers = config['kafka']['kafkaServers']
        self.producer = KafkaProducer(
            bootstrap_servers=self.kafka_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda v: v if isinstance(v, bytes) else v.encode('utf-8')
        )

    @staticmethod
    def get_coin_data(symbol):
        url = f'https://api.binance.com/api/v3/ticker/24hr'
        params = {'symbol': symbol.upper()}

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération des données pour {symbol}: {e}")
            return None

        return response.json()

    def process_coin_data(self, symbol):
        data = self.get_coin_data(symbol)
        if not data:
            return

        coin_data = {
            "symbol": symbol,
            "price_change": data.get("priceChange"),
            "price_change_percent": data.get("priceChangePercent"),
            "weighted_avg_price": data.get("weightedAvgPrice"),
            "last_price": data.get("lastPrice"),
            "volume": data.get("volume"),
            "quote_volume": data.get("quoteVolume"),
            "high_price": data.get("highPrice"),
            "low_price": data.get("lowPrice"),
            "open_price": data.get("openPrice")
        }

        self.producer.send(
            self.topic,
            key=symbol.encode('utf-8'),
            value=coin_data
        )
        print(f"Coin Datas : {coin_data}")

    def start(self):
        try:
            while True:
                for symbol in self.symbols:
                    self.process_coin_data(symbol)
                    time.sleep(1)
                time.sleep(60)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        print('Interruption reçue, fermeture du producteur Kafka.')
        if self.producer:
            self.producer.close()
        sys.exit(0)


if __name__ == "__main__":
    symbols = ['btcusdt', 'ethusdt', 'bnbusdt']

    producer = CoinMarketCapProducer(symbols=symbols)

    try:
        producer.start()
    except KeyboardInterrupt:
        producer.stop()