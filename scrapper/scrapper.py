import configparser
from kafka import KafkaAdminClient
from kafka.admin import NewTopic

config = configparser.ConfigParser()

# Load the configuration file
config.read("config.ini")

# Create a Kafka admin client
admin_client = KafkaAdminClient(bootstrap_servers="kafka:9092")

# List all topics
topics = admin_client.list_topics()

# Create topics
topic_in_binance = NewTopic(
    name=config['kafka']['TopicIn_Binance'],
    num_partitions=int(config['kafka']['TopicInPartitions_Binance']),
    replication_factor=int(config['kafka']['TopicInReplication_Binance'])
)
topic_out_binance = NewTopic(
    name=config['kafka']['TopicOut_Binance'],
    num_partitions=int(config['kafka']['TopicOutPartitions_Binance']),
    replication_factor=int(config['kafka']['TopicOutReplication_Binance'])
)
topic_in_rssfeed = NewTopic(
    name=config['kafka']['TopicIn_RSSfeed'],
    num_partitions=int(config['kafka']['TopicInPartitions_RSSfeed']),
    replication_factor=int(config['kafka']['TopicInReplication_RSSfeed'])
)
topic_out_rssfeed = NewTopic(
    name=config['kafka']['TopicOut_RSSfeed'],
    num_partitions=int(config['kafka']['TopicOutPartitions_RSSfeed']),
    replication_factor=int(config['kafka']['TopicOutReplication_RSSfeed'])
)

new_topics = [topic_in_binance, topic_out_binance, topic_in_rssfeed, topic_out_rssfeed]

for topic in new_topics:
    if topic.name not in topics:
        admin_client.create_topics([topic])

# Delete a topic
# admin_client.delete_topics([config['kafka']['TopicInName'], config['kafka']['TopicOutName']])

# Close the client
admin_client.close()