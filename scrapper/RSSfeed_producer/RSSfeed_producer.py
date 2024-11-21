# RSSfeed_producer.py
import configparser
import json
import sys
import time
import threading
import feedparser
from kafka import KafkaProducer
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


class RSSFeedProducer:
    def __init__(self, feed_urls=None, config_file='config.ini', polling_interval=60):
        config = configparser.ConfigParser()
        config.read(config_file)
        if feed_urls is None:
            feed_urls = eval(config['rss']['feedUrls'])
        self.feed_urls = feed_urls
        self.topic = config['kafka']['TopicIn_RSSfeed']
        self.kafka_servers = config['kafka']['kafkaServers']
        self.polling_interval = polling_interval
        self.producer = None
        self.seen_entries = set()

    def start(self):
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=self.kafka_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda v: v if isinstance(v, bytes) else v.encode('utf-8')
            )

            logging.info("Kafka producer initialized successfully.")
        except Exception as e:
            logging.error(f"Failed to initialize Kafka producer: {e}")
            sys.exit(1)

        try:
            while True:
                self.fetch_and_send_feeds()
                time.sleep(self.polling_interval)
        except KeyboardInterrupt:
            self.stop()
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            self.stop()

    def fetch_and_send_feeds(self):
        for url in self.feed_urls:
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries:
                    entry_id = entry.get('id', entry.get('link'))
                    if entry_id not in self.seen_entries:
                        self.seen_entries.add(entry_id)
                        message = {
                            'title': entry.get('title'),
                            'link': entry.get('link'),
                            'published': entry.get('published'),
                            'summary': entry.get('summary'),
                            'source': feed.feed.get('title', url)
                        }
                        key = entry_id.encode('utf-8')
                        self.producer.send(
                            self.topic,
                            key=key,
                            value=message
                        )
                        logging.info(f"Sent entry {entry_id} to topic {self.topic}")
            except Exception as e:
                logging.error(f"Error processing feed {url}: {e}")

    def stop(self):
        print('Interruption reçue, fermeture du producteur Kafka.')
        if self.producer:
            self.producer.close()
        sys.exit(0)


if __name__ == "__main__":
    producer = RSSFeedProducer(polling_interval=60)

    try:
        producer.start()
    except KeyboardInterrupt:
        producer.stop()