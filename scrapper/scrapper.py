from kafka import KafkaAdminClient
from kafka.admin import NewTopic

admin_client = KafkaAdminClient(bootstrap_servers="kafka:9092")

# Create a topic
example_topic = NewTopic(name="example-topic", num_partitions=1, replication_factor=1)
admin_client.create_topics([example_topic])

# List all topics
topics = admin_client.list_topics()
print(topics)

# Delete a topic
admin_client.delete_topics(["example-topic"])

# Close the client
admin_client.close()