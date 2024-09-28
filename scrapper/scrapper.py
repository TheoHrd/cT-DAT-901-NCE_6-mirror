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
topic_in = NewTopic(
    name=config['kafka']['TopicInName'],
    num_partitions=int(config['kafka']['TopicInPartitions']),
    replication_factor=int(config['kafka']['TopicInReplication'])
)
topic_out = NewTopic(
    name=config['kafka']['TopicOutName'],
    num_partitions=int(config['kafka']['TopicOutPartitions']),
    replication_factor=int(config['kafka']['TopicOutReplication'])
)

new_topics = [topic_in, topic_out]

for topic in new_topics:
    if topic.name not in topics:
        admin_client.create_topics([topic])

# Delete a topic
# admin_client.delete_topics([config['kafka']['TopicInName'], config['kafka']['TopicOutName']])

# Close the client
admin_client.close()