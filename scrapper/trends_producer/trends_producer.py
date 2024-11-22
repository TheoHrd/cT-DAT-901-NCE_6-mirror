# trends_producer.py

import configparser
import json
import sys
import time
import random
from kafka import KafkaProducer
from pytrends.request import TrendReq
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


class TrendsProducer:
    def __init__(self, keywords=None, config_file='config.ini', interval=900):  # Intervalle de 15 minutes
        config = configparser.ConfigParser()
        config.read(config_file)
        if keywords is None:
            keywords = eval(config['crypto']['cryptoNames'].lower())

        self.keywords = keywords
        self.topic = config['kafka']['TopicIn_Trends']
        self.kafka_servers = config['kafka']['kafkaServers']
        self.interval = interval
        self.producer = None


    def start(self):
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=self.kafka_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda v: v.encode('utf-8') if isinstance(v, str) else v
            )
            logging.info("Kafka producer initialized successfully.")
        except Exception as e:
            logging.error(f"Failed to initialize Kafka producer: {e}")
            sys.exit(1)

        try:
            while True:
                self.fetch_and_send_trends()
                time.sleep(self.interval)
        except KeyboardInterrupt:
            self.stop()
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            self.stop()

    def fetch_and_send_trends(self):
        chunk_size = 5
        keyword_chunks = [self.keywords[i:i + chunk_size] for i in range(0, len(self.keywords), chunk_size)]

        for chunk in keyword_chunks:
            success = False
            backoff_time = 60
            max_backoff_time = 3600

            while not success:
                try:
                    self.pytrends = TrendReq(
                        hl='en-US',
                        tz=0,
                        requests_args={
                            'headers': {
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                            }
                        }
                    )
                    self.pytrends.build_payload(chunk, timeframe='now 4-H')
                    interest_over_time = self.pytrends.interest_over_time()
                    if not interest_over_time.empty:
                        if 'isPartial' in interest_over_time.columns:
                            interest_over_time = interest_over_time.drop(columns=['isPartial'])

                        for timestamp, row in interest_over_time.iterrows():
                            data = row.to_dict()
                            data['timestamp'] = timestamp.isoformat()
                            data['keywords'] = chunk
                            key = str(timestamp.timestamp()).encode('utf-8')
                            self.producer.send(
                                self.topic,
                                key=key,
                                value=data
                            )
                            logging.info(f"Sent trends data for {timestamp} and keywords {chunk} to topic {self.topic}")
                        success = True
                    else:
                        logging.warning(f"No trend data received for keywords: {chunk}")
                        success = True
                except Exception as e:
                    logging.error(f"Error fetching trends data for keywords {chunk}: {e}")
                    if '429' in str(e):
                        logging.warning(f"Received 429 error, sleeping for {backoff_time} seconds before retrying.")
                        time.sleep(backoff_time)
                        backoff_time = min(max_backoff_time, backoff_time * 2)
                    else:
                        logging.error("An unexpected error occurred.")
                        success = True

    def stop(self):
        logging.info('Interruption reçue, fermeture du producteur Kafka.')
        if self.producer:
            self.producer.close()
        sys.exit(0)


if __name__ == "__main__":
    producer = TrendsProducer(interval=900)
    try:
        producer.start()
    except KeyboardInterrupt:
        producer.stop()
