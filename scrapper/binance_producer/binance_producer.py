# binance_producer.py
import configparser
import json
import sys
import time
import threading
import websocket
from kafka import KafkaProducer
import requests


class BinanceProducer:
    def __init__(self, symbols=None, config_file='config.ini'):

        if symbols is None:
            symbols = ['btcusdt']

        config = configparser.ConfigParser()
        config.read(config_file)
        self.symbols = [str(symbol).lower() for symbol in symbols]
        self.topic = config['kafka']['TopicIn_Binance']
        self.kafka_servers = config['kafka']['kafkaServers']
        self.producer = None
        self.ws_connections = []

    def on_message(self, ws, message):
        message_json = json.loads(message)
        data = message_json.get('data')

        if data is None:
            print(f"Message inattendu : {message_json}")
            return

        symbol = data.get('s')

        if symbol is None:
            print(f"Symbole manquant dans les données : {data}")
            return

        print(f"Data received for {symbol}: {data}")

        data['symbol'] = symbol

        key = symbol.encode('utf-8')

        self.producer.send(
            self.topic,
            key=key,
            value=data
        )

    def on_error(self, ws, error):
        print(f"Erreur : {error}")

    def on_close(self, ws, close_status_code, close_msg):
        print(f"### Connexion fermée ### Code: {close_status_code}, Message: {close_msg}")

    def on_open(self, ws):
        print("### Connexion ouverte ###")

    def start(self):
        self.producer = KafkaProducer(
            bootstrap_servers=self.kafka_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda v: v if isinstance(v, bytes) else v.encode('utf-8')
        )

        chunk_size = 100
        symbol_chunks = [self.symbols[i:i + chunk_size] for i in range(0, len(self.symbols), chunk_size)]

        threads = []
        for chunk in symbol_chunks:
            thread = threading.Thread(target=self._start_socket, args=(chunk,))
            thread.daemon = True
            threads.append(thread)
            thread.start()
            time.sleep(1)

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def _start_socket(self, symbols_chunk):
        streams = '/'.join([f"{symbol}@trade" for symbol in symbols_chunk])
        ws_url = f"wss://stream.binance.com:9443/stream?streams={streams}"
        ws = websocket.WebSocketApp(
            ws_url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        self.ws_connections.append(ws)
        ws.run_forever()

    def stop(self):
        print('Interruption reçue, fermeture des WebSockets et du producteur Kafka.')
        for ws in self.ws_connections:
            ws.close()
        if self.producer:
            self.producer.close()
        sys.exit(0)


def get_usdt_pairs():
    url = 'https://api.binance.com/api/v3/exchangeInfo'
    response = requests.get(url)
    data = response.json()
    usdt_pairs = []
    for symbol in data['symbols']:
        if symbol['quoteAsset'] == 'USDT' and symbol['status'] == 'TRADING':
            usdt_pairs.append(symbol['symbol'].lower())
    return usdt_pairs

if __name__ == "__main__":

    # Get available USDT pairs on Binance
    available_pairs = get_usdt_pairs()

    # Get Cryptocurrencies from config
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    # Make USDT pairs from config
    pairs = [f'{symbol}usdt' for symbol in eval(config['crypto']['cryptoSymbols'].lower())]

    # Final list is the pairs from config that are available on Binance
    symbols = list(set(available_pairs) & set(pairs))

    # print(symbols)

    producer = BinanceProducer(symbols=symbols)

    try:
        producer.start()
    except KeyboardInterrupt:
        producer.stop()

