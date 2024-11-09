# binance_producer.py

import json
import sys
import time
import threading
import websocket
from kafka import KafkaProducer
import requests


class BinanceProducer:
    def __init__(self, symbolsList=None, topic='entries_raw', bootstrap_servers='kafka:9092'):
        if symbols is None:
            symbols = ['btcusdt', 'etcusdt', 'bnbusdt', 'xprusdt', 'solusdt', 'trxusdt']
        self.symbols = [str(symbol).lower() for symbol in symbols]
        self.topic = topic
        self.bootstrap_servers = bootstrap_servers
        self.producer = None
        self.ws_connections = {}

    def on_message(self, ws, message):
        message_json = json.loads(message)
        stream = message_json.get('stream')
        data = message_json.get('data')
        symbol = data['symbol']

        print(f"Data received for {symbol}: {data}")

        data['symbol'] = symbol

        key = symbol.encode('utf-8')

        self.producer.send(
            self.topic,
            key=key,
            value=data
        )

    @staticmethod
    def on_error(error):
        print(f"Erreur : {error}")

    @staticmethod
    def on_close(ws, close_status_code, close_msg):
        print("### Connexion fermée ###")

    @staticmethod
    def on_open(ws):
        print("### Connexion ouverte ###")

    def start(self):
        self.producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda v: v if isinstance(v, bytes) else v.encode('utf-8')
        )

        streams = '/'.join([f"{symbol}@trade" for symbol in self.symbols])
        ws_url = f"wss://stream.binance.com:9443/stream?streams={streams}"
        ws = websocket.WebSocketApp(
            ws_url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        ws.run_forever()

    def stop(self):
        print('Interruption reçue, fermeture des WebSockets et du producteur Kafka.')
        for symbol, ws in self.ws_connections.items():
            ws.close()
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

    symbols_hard_coded = [
        'btcusdt', 'ethusdt', 'bnbusdt', 'xrpusdt', 'adausdt', 'solusdt', 'dogeusdt', 'maticusdt', 'dotusdt', 'ltcusdt',
        'shibusdt', 'trxusdt', 'avaxusdt', 'uniusdt', 'linkusdt', 'atomusdt', 'xlmusdt', 'ftmusdt', 'bchusdt',
        'algousdt',
        'vetusdt', 'egldusdt', 'icpusdt', 'filusdt', 'hbarusdt', 'sandusdt', 'manausdt', 'thetausdt', 'aaveusdt',
        'axsusdt',
        'wavesusdt', 'compusdt', 'zecusdt', 'dashusdt', 'nearusdt', 'chzusdt', 'enjusdt', 'oneusdt', 'galausdt',
        'iotxusdt',
        'rvnusdt', 'arusdt', 'crvusdt', 'sushiusdt', 'batusdt', 'omgusdt', 'dydxusdt', 'ankrusdt', 'ontusdt', 'zilusdt'
    ]

    producer = BinanceProducer(symbolsList=symbols, topic='entries_raw', bootstrap_servers='kafka:9092')
    try:
        producer.start()
    except KeyboardInterrupt:
        producer.stop()

