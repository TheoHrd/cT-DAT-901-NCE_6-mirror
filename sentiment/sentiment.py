import configparser
from kafka import KafkaConsumer, KafkaProducer
import json
from textblob import TextBlob
import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def get_sentiment(text):
    analysis = TextBlob(text)
    return (analysis.sentiment.polarity, analysis.sentiment.subjectivity)

config = configparser.ConfigParser()
# Load the configuration file
config.read("config.ini")

# Make a list of symbol and names of currencies from configuration file
currencies = [
    {"symbol": x[0], "name": x[1]}
    for x in
    zip(
        eval(config['crypto']['cryptoSymbols']),
        eval(config['crypto']['cryptoNames']))
]

# Create a Kafka consumer
consumer = KafkaConsumer(
    config['kafka']['TopicIn_RSSfeed'],
    bootstrap_servers=config['kafka']['kafkaServers'],
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    key_deserializer=lambda v: v.decode('utf-8')
)

# Create a Kafka producer
producer = KafkaProducer(
    bootstrap_servers=config['kafka']['kafkaServers'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    key_serializer=lambda v: v if isinstance(v, bytes) else v.encode('utf-8')
)

# Poll for new messages
try:
    while(True):
        for message in consumer:
            
            ignore_title = False
            ignore_summary = False
            sentiment = 0.0
            subjects = []
            entry = dict()

            if(message is None):
                continue
            
            for currency in currencies:
                if currency["symbol"].lower() in message.value["title"].lower() \
                or currency["name"].lower() in message.value["title"].lower():
                    subjects.append(currency["symbol"])
                    print(f"Currency: {currency['name']}")
                elif currency["symbol"].lower() in message.value["summary"].lower() \
                or currency["name"].lower() in message.value["summary"].lower():
                    subjects.append(currency["symbol"])
                    print(f"Currency: {currency['name']}")
                    
            if subjects == []:
                continue
                    
            # print(message.value)

            sentiment_title = get_sentiment(message.value["title"])
            sentiment_summary = get_sentiment(message.value["summary"])
            
            # print(f"Title Sentiment: {sentiment_title}")
            # print(f"Summary Sentiment: {sentiment_summary}")
            
            if(sentiment_title[0] == 0.0 and sentiment_title[1] == 0.0):
                ignore_title = True
            if(sentiment_summary[0] == 0.0 and sentiment_summary[1] == 0.0):
                ignore_summary = True
                
            if(ignore_title and ignore_summary):
                # Both title and summary full neutral, return neutral
                sentiment = 0.0
            elif(ignore_title):
                # Title is neutral, return summary sentiment
                sentiment = sentiment_summary[0] * (1 - sentiment_summary[1])
            elif(ignore_summary):
                # Summary is neutral, return title sentiment
                sentiment = sentiment_title[0] * (1 - sentiment_title[1])
            else:
                # Both title and summary have sentiment, return average
                sentiment = (sentiment_title[0] * (1 - sentiment_title[1]) + sentiment_summary[0] * (1 - sentiment_summary[1])) / 2
            # print(f"Sentiment: {sentiment}")

            # Prepare entries for sentiment analysis
            for subject in subjects:
                entry["subject"] = subject
                entry["sentiment"] = sentiment
                # Date to unix timestamp
                try:
                    entry["date"] = datetime.datetime.strptime(message.value["published"], "%a, %d %b %Y %H:%M:%S %z").timestamp()
                except:
                    # If we can't figure out time, discard entry
                    continue

                # print(json.dumps(entry, indent=4))
                
                # Send the sentiment to the output topic
                producer.send(config['kafka']['TopicOut_RSSfeed'], key=message.key, value=entry)
                logging.info(f"Sentiment for {entry['subject']} sent to topic {config['kafka']['TopicOut_RSSfeed']}")

            print("=====================================")
except KeyboardInterrupt:
    consumer.close()